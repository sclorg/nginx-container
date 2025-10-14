import pytest


from pathlib import Path
from container_ci_suite.container_lib import ContainerTestLib
from container_ci_suite.engines.podman_wrapper import PodmanCLIWrapper
from conftest import VARS

test_app = VARS.TEST_DIR / "test-app"


def build_s2i_app(app_path: Path) -> ContainerTestLib:
    container_lib = ContainerTestLib(VARS.IMAGE_NAME)
    app_name = app_path.name
    s2i_app = container_lib.build_as_df(
        app_path=app_path,
        s2i_args="--pull-policy=never",
        src_image=VARS.IMAGE_NAME,
        dst_image=f"{VARS.IMAGE_NAME}-{app_name}"
    )
    return s2i_app


class TestNginxApplicationContainer:

    def setup_method(self):
        self.s2i_app = build_s2i_app(app_path=test_app)

    def teardown_method(self):
        self.s2i_app.cleanup()

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
        cid_file_name = "test-app"
        assert self.s2i_app.create_container(
            cid_file_name=cid_file_name,
            container_args=f"--user 10001 {container_arg}"
        )
        cip = self.s2i_app.get_cip(cid_file_name=cid_file_name)
        assert cip
        # nginx -v returns proper version
        assert f"nginx/{VARS.VERSION_NO_MICRO}" in PodmanCLIWrapper.podman_run_command_and_remove(
            cid_file_name=f"{VARS.IMAGE_NAME}-{cid_file_name}",
            cmd="nginx -v"
        )
        # Response code from HTTP url is 200 and contains proper output
        assert self.s2i_app.test_response(
            url=f"http://{cip}", expected_output="NGINX is working"
        )
        # Response code from HTTP url is 200 and contains proper output
        assert self.s2i_app.test_response(
            url=f"http://{cip}", expected_output="NGINX2 is working",
            host="localhost2"
        )
        # Response code from HTTP url is 200 and contains proper output
        assert self.s2i_app.test_response(
            url=f"http://{cip}", expected_output="NGINX2 is working",
            page="/aliased/index2.html"
        )
        # Response code from HTTP url is 404 and nginx-cfg/default.conf is not accessible
        assert self.s2i_app.test_response(
            url=f"http://{cip}", expected_code=404,
            page="/nginx-cfg/default.conf"
        )
