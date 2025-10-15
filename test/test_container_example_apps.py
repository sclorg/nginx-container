import pytest
import re

from pathlib import Path

from container_ci_suite.container_lib import ContainerTestLib
from container_ci_suite.engines.podman_wrapper import PodmanCLIWrapper
from container_ci_suite.engines.container import ContainerImage

from conftest import VARS

test_app = VARS.TEST_DIR / "test-app"
perl_test_app = VARS.TEST_DIR / "perl-test-app"
start_hook_test_app = VARS.TEST_DIR / "start-hook-test-app"


def build_s2i_app(app_path: Path) -> ContainerTestLib:
    """
    Build S2I Container based on the app_path input
    :param: app_path: path to example directory
    :return new instance of ContainerTestLib
    """
    container_lib = ContainerTestLib(VARS.IMAGE_NAME)
    app_name = app_path.name
    s2i_app = container_lib.build_as_df(
        app_path=app_path,
        s2i_args="--pull-policy=never",
        src_image=VARS.IMAGE_NAME,
        dst_image=f"{VARS.IMAGE_NAME}-{app_name}"
    )
    s2i_app.set_new_image(image_name=f"{VARS.IMAGE_NAME}-{app_name}")
    return s2i_app


class TestNginxExampleAppContainer:

    def setup_method(self):
        self.s2i_app = build_s2i_app(start_hook_test_app)

    def teardown_method(self):
        self.s2i_app.cleanup()

    def test_run_app_test(self):
        cid_file_name = self.s2i_app.app_name
        # Create container with --user 10001
        assert self.s2i_app.create_container(cid_file_name=cid_file_name, container_args="--user 10001")
        # Wait till container does not start
        assert ContainerImage.wait_for_cid(cid_file_name=cid_file_name)
        cid = self.s2i_app.get_cid(cid_file_name=cid_file_name)
        assert cid
        cip = self.s2i_app.get_cip(cid_file_name=cid_file_name)
        assert cip
        command = PodmanCLIWrapper.podman_get_file_content(
            cid_file_name=cid, filename="/opt/app-root/etc/nginx.d/default.conf"
        )
        # Checks if nginx configuration contains resolver
        assert re.search("resolver", command)
        # Checks if nginx configuration DO NOT container "DNS_SERVER"
        assert not re.search("DNS_SERVER", command)
        assert f"nginx/{VARS.VERSION_NO_MICRO}" in PodmanCLIWrapper.podman_run_command_and_remove(
            cid_file_name=VARS.IMAGE_NAME,
            cmd="nginx -v"
        )
        assert self.s2i_app.test_response(
            url=f"http://{cip}", expected_output="NGINX is working"
        )
        assert self.s2i_app.test_response(
            url=f"http://{cip}", expected_output="NGINX2 is working",
            host="localhost2"
        )
        assert self.s2i_app.test_response(
            url=f"http://{cip}", expected_code=404,
            page="/nginx-cfg/default.conf"
        )


class TestNginxExamplePerlAppContainer:

    def setup_method(self):
        self.s2i_app = build_s2i_app(perl_test_app)

    def teardown_method(self):
        self.s2i_app.cleanup()

    def test_run_app_test(self):
        if VARS.VERSION.endswith("-micro"):
            pytest.skip("Run the chosen tests (not for micro variant which lacks perl)")
        cid_file_name = self.s2i_app.app_name
        self.s2i_app.set_new_image(image_name=f"{VARS.IMAGE_NAME}-{cid_file_name}")
        assert self.s2i_app.create_container(cid_file_name=cid_file_name, container_args="--user 10001")
        cid = self.s2i_app.get_cid(cid_file_name=cid_file_name)
        assert cid
        cip = self.s2i_app.get_cip(cid_file_name=cid_file_name)
        assert cip
        # Checks if returns header of Perl version
        perl_version = PodmanCLIWrapper.podman_exec_shell_command(cid_file_name=cid, cmd="perl -e 'print \"$^V\"'")
        assert self.s2i_app.test_response(
            url=f"http://{cip}", port=8080,
            expected_output=f"X-Perl-Version: {perl_version}"
        )
        assert self.s2i_app.test_response(
            url=f"http://{cip}", port=8080, page="/perl", expected_output="Perl location handler is working"
        )


class TestNginxLogContainer:

    def setup_method(self):
        self.s2i_app = build_s2i_app(test_app)

    def teardown_method(self):
        self.s2i_app.cleanup()

    def test_log_output(self):
        """
        Test checks if logging container works properly
        and logs contain proper output
        """
        cid_file_name = "test-app"
        self.s2i_app.set_new_image(image_name=f"{VARS.IMAGE_NAME}-{cid_file_name}")
        assert self.s2i_app.create_container(
            cid_file_name=cid_file_name,
            container_args="--user 10001"
        )
        cid = self.s2i_app.get_cid(cid_file_name=cid_file_name)
        assert cid
        cip = self.s2i_app.get_cip(cid_file_name=cid_file_name)
        assert self.s2i_app.test_response(
            url=f"http://{cip}", port=8080, expected_output="NGINX is working"
        )
        assert '"GET / HTTP/1.1" 200' in self.s2i_app.get_logs(cid_file_name=cid_file_name)
        # Check if /nothing-at-all is really no accessible
        assert self.s2i_app.test_response(
            url=f"http://{cip}", port=8080, page="/nothing-at-all", expected_code=404
        )
        logs = self.s2i_app.get_logs(cid_file_name=cid_file_name)
        assert logs
        # Checks logs container 'failed' and 'No such file or directory'
        assert re.search("open.*failed.*No such file or directory", logs)

    def test_log_volume_output(self):
        """
        Test checks if logging container works properly
        and logs contain proper output.
        The logs are mounted from host and so we check
        the logs in host directly
        """
        cid_file_name = "test-app"
        self.s2i_app.set_new_image(image_name=f"{VARS.IMAGE_NAME}-{cid_file_name}")
        assert self.s2i_app.create_container(
            cid_file_name=cid_file_name,
            container_args="-e NGINX_LOG_TO_VOLUME=y --user 10001"
        )
        cid = self.s2i_app.get_cid(cid_file_name=cid_file_name)
        assert cid
        cip = self.s2i_app.get_cip(cid_file_name=cid_file_name)
        assert self.s2i_app.test_response(url=f"http://{cip}", port=8080, expected_output="NGINX is working")
        assert '"GET / HTTP/1.1" 200' in PodmanCLIWrapper.podman_get_file_content(
            cid_file_name=cid,
            filename="/var/log/nginx/access.log"
        )
        # Check if /nothing-at-all is really no accessible
        assert self.s2i_app.test_response(
            url=f"http://{cip}", port=8080, page="/nothing-at-all", expected_code=404
        )
        # Check if /nothing-at-all is really mentioned in 'access.log'
        assert '"GET /nothing-at-all HTTP/1.1" 404' in PodmanCLIWrapper.podman_get_file_content(
            cid_file_name=cid,
            filename="/var/log/nginx/access.log"
        )
        logs_to_check = PodmanCLIWrapper.podman_get_file_content(
            cid_file_name=cid,
            filename="/var/log/nginx/error.log"
        )
        # Checks logs container 'failed' and 'No such file or directory'
        assert re.search("open.*failed.*No such file or directory", logs_to_check)
