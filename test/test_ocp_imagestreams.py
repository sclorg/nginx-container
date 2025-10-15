from container_ci_suite.imagestreams import ImageStreamChecker

from conftest import VARS


class TestLatestImagestreams:

    def setup_method(self):
        self.isc = ImageStreamChecker(working_dir=VARS.TEST_DIR / ".." / "..")

    def test_latest_imagestream(self):
        """
        Test checks we have the latest imagestream in GitHub repository
        """
        self.latest_version = self.isc.get_latest_version()
        assert self.latest_version != ""
        self.isc.check_imagestreams(self.latest_version)
