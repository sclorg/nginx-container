import pytest


from pathlib import Path
from container_ci_suite.container_lib import ContainerTestLib
from container_ci_suite.engines.podman_wrapper import PodmanCLIWrapper
from constants import TEST_DIR, IMAGE_NAME, VERSION

test_app = TEST_DIR / "test-app"


def build_s2i_app(app_path: Path) -> ContainerTestLib:
    container_lib = ContainerTestLib(IMAGE_NAME)
    app_name = app_path.name
    s2i_app = container_lib.build_as_df(
        app_path=app_path,
        s2i_args="--pull-policy=never",
        src_image=IMAGE_NAME,
        dst_image=f"{IMAGE_NAME}-{app_name}"
    )
    return s2i_app


class TestNginxApplicationContainer:

    def setup_method(self):
        self.app = ContainerTestLib(image_name=IMAGE_NAME, s2i_image=True)

    def teardown_method(self):
        self.app.cleanup()

    @pytest.mark.parametrize(
        "container_arg",
        [
            "",
            "--user 12345"
        ]
    )
    def test_application(self, container_arg):
        """
        Test if container works under specific user
        and not only with user --user 10001
        """
        version = VERSION.replace("-micro", "")
        cid_file_name = "test-app"
        assert self.app.create_container(
            cid_file_name=cid_file_name,
            container_args=f"--user 10001 {container_arg}"
        )
        cip = self.app.get_cip(cid_file_name=cid_file_name)
        assert cip
        # nginx -v returns proper version
        assert PodmanCLIWrapper.podman_run_command(
            f"--rm {self.app.image_name} /bin/bash -c 'nginx -v'"
        ).startswith(f"nginx version: nginx/{version}")
        # Response code from HTTP url is 200 and contains proper output
        assert self.app.test_response(
            url=f"http://{cip}", expected_output="NGINX is working"
        )
        # Response code from HTTP url is 200 and contains proper output
        assert self.app.test_response(
            url=f"http://{cip}", expected_output="NGINX2 is working",
            host="localhost2"
        )
        # Response code from HTTP url is 200 and contains proper output
        assert self.app.test_response(
            url=f"http://{cip}", expected_output="NGINX2 is working",
            page="/aliased/index2.html"
        )
        # Response code from HTTP url is 404 and nginx-cfg/default.conf is not accessible
        assert self.app.test_response(
            url=f"http://{cip}", expected_code=404,
            page="/nginx-cfg/default.conf"
        )
