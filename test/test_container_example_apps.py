import pytest
import re

from pathlib import Path

from container_ci_suite.container_lib import ContainerTestLib
from container_ci_suite.engines.podman_wrapper import PodmanCLIWrapper
from container_ci_suite.engines.container import ContainerImage

from constants import TEST_DIR, IMAGE_NAME, VERSION

test_app = TEST_DIR / "test-app"
perl_test_app = TEST_DIR / "perl-test-app"
start_hook_test_app = TEST_DIR / "start-hook-test-app"


def build_s2i_app(app_path: Path) -> ContainerTestLib:
    container_lib = ContainerTestLib(IMAGE_NAME)
    app_name = app_path.name
    s2i_app = container_lib.build_as_df(
        app_path=app_path,
        s2i_args="--pull-policy=never",
        src_image=IMAGE_NAME,
        dst_image=f"{IMAGE_NAME}-{app_name}"
    )
    s2i_app.set_new_image(image_name=f"{IMAGE_NAME}-{app_name}")
    return s2i_app


class TestNginxExampleAppContainer:

    def setup_method(self):
        self.s2i_app = build_s2i_app(start_hook_test_app)

    def teardown_method(self):
        self.s2i_app.cleanup()

    def test_run_app_test(self, example_app_test):
        version = VERSION.replace("-micro", "")
        cid_file_name = example_app_test.app_name
        assert self.s2i_app.create_container(cid_file_name=cid_file_name, container_args="--user 10001")
        assert ContainerImage.wait_for_cid(cid_file_name=cid_file_name)
        cid = self.s2i_app.get_cid(cid_file_name=cid_file_name)
        assert cid
        cip = self.s2i_app.get_cip(cid_file_name=cid_file_name)
        assert cip
        command = PodmanCLIWrapper.podman_get_file_content(
            cid_file_name=cid, filename="/opt/app-root/etc/nginx.d/default.conf"
        )
        assert re.search("resolver", command)
        assert not re.search("DNS_SERVER", command)
        assert PodmanCLIWrapper.podman_run_command(
            f"--rm {example_app_test.image_name} /bin/bash -c 'nginx -v'"
        ).startswith(f"nginx version: nginx/{version}")
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
        if VERSION.endswith("-micro"):
            pytest.skip("Run the chosen tests (not for micro variant which lacks perl)")
        cid_file_name = self.s2i_app.app_name
        self.s2i_app.set_new_image(image_name=f"{IMAGE_NAME}-{cid_file_name}")
        assert self.s2i_app.create_container(cid_file_name=cid_file_name, container_args="--user 10001")
        cid = self.s2i_app.get_cid(cid_file_name=cid_file_name)
        assert cid
        cip = self.s2i_app.get_cip(cid_file_name=cid_file_name)
        assert cip
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

    # test_log_output
    def test_log_output(self, s2i_log_test):
        cid_file_name = "test-app"
        s2i_log_test.set_new_image(image_name=f"{IMAGE_NAME}-{cid_file_name}")
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
        assert '"GET / HTTP/1.1" 200' in s2i_log_test.get_logs(cid_file_name=cid_file_name)
        assert self.s2i_app.test_response(
            url=f"http://{cip}", port=8080, page="/nothing-at-all", expected_code=404
        )
        logs = self.s2i_app.get_logs(cid_file_name=cid_file_name)
        assert logs
        assert re.search("open.*failed.*No such file or directory", logs)

    # test_log_volume_output
    def test_log_volume_output(self, s2i_log_test):
        cid_file_name = "test-app"
        s2i_log_test.set_new_image(image_name=f"{IMAGE_NAME}-{cid_file_name}")
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
        assert self.s2i_app.test_response(
            url=f"http://{cip}", port=8080, page="/nothing-at-all", expected_code=404
        )
        assert '"GET /nothing-at-all HTTP/1.1" 404' in PodmanCLIWrapper.podman_get_file_content(
            cid_file_name=cid,
            filename="/var/log/nginx/access.log"
        )
        logs_to_check = PodmanCLIWrapper.podman_get_file_content(
            cid_file_name=cid,
            filename="/var/log/nginx/error.log"
        )
        assert re.search("open.*failed.*No such file or directory", logs_to_check)

