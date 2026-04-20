import pytest

from container_ci_suite.container_lib import ContainerTestLib
from container_ci_suite.compare_images import ContainerCompareClass
from container_ci_suite.utils import get_public_image_name, get_previous_os_version

from conftest import VARS


class TestNginxContainerSizes:
    """
    Test container sizes
    """

    def setup_method(self):
        """
        Setup method
        """
        self.app = ContainerTestLib(image_name=VARS.IMAGE_NAME, s2i_image=True)

    def teardown_method(self):
        """
        Teardown method
        """
        self.app.cleanup()

    def test_compare_container_sizes(self):
        """
        Test the size of the Nginx container against the
        already published container images.
        """
        if not VARS.OS.startswith("rhel"):
            pytest.skip("Skipping container size comparison for non-RHEL OS.")
        published_image_name = get_public_image_name(
            os_name=get_previous_os_version(VARS.OS),
            base_image_name="nginx",
            version=VARS.VERSION,
            stage_registry=True,
        )
        is_less_uncopressed = ContainerCompareClass.is_uncompressed_image_smaller(
            built_image_name=VARS.IMAGE_NAME,
            published_image=published_image_name,
        )
        is_less_compressed = ContainerCompareClass.is_compressed_image_smaller(
            built_image_name=VARS.IMAGE_NAME,
            published_image_name=published_image_name,
        )
        if not is_less_uncopressed or not is_less_compressed:
            pytest.skip(
                f"Container size is not less than the published image {published_image_name}. "
                f"Uncompressed image size: {is_less_uncopressed}, Compressed image size: {is_less_compressed}"
            )
