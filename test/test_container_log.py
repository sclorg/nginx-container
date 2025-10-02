import os
import sys
import pytest

from pathlib import Path

from container_ci_suite.container_lib import ContainerTestLib
from container_ci_suite.engines.podman_wrapper import PodmanCLIWrapper
from container_ci_suite.utils import check_variables, ContainerTestLibUtils, get_file_content


if not check_variables():
    print("At least one variable from OS, VERSION is missing.")
    sys.exit(1)
TEST_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
VERSION = os.getenv("VERSION")
OS = os.getenv("TARGET").lower()
IMAGE_NAME = os.getenv("IMAGE_NAME")
if not IMAGE_NAME:
    print(f"Built container for version {VERSION} on OS {OS} does not exist.")
    sys.exit(1)
test_app = os.path.join(TEST_DIR, "test-app")


@pytest.fixture(scope="module", params=[test_app])
def s2i_log_test(request):
    container_lib = ContainerTestLib(IMAGE_NAME)
    app_name = os.path.basename(request.param)
    s2i_app = container_lib.build_as_df(
        app_path=request.param,
        s2i_args="--pull-policy=never",
        src_image=IMAGE_NAME,
        dst_image=f"{IMAGE_NAME}-{app_name}"
    )
    yield s2i_app
    s2i_app.clean_containers()


class TestNginxLogContainer:

    # test_log_output
    def test_log_output(self, s2i_log_test):
        cid_file_name = "test-app"
        s2i_log_test.set_new_image(image_name=f"{IMAGE_NAME}-{cid_file_name}")
        assert s2i_log_test.create_container(
            cid_file_name=cid_file_name,
            container_args=f"--user 10001"
        )
        cid = s2i_log_test.get_cid(cid_file_name=cid_file_name)
        assert cid
        cip = s2i_log_test.get_cip(cid_file_name=cid_file_name)
        assert s2i_log_test.test_response(
            url=f"http://{cip}", port=8080, expected_output="NGINX is working"
        )
        assert '"GET / HTTP/1.1" 200' in s2i_log_test.get_logs(cid_file_name=cid_file_name)
        assert s2i_log_test.test_response(
            url=f"http://{cip}", port=8080, page="/nothing-at-all", expected_code=404
        )
        logs = s2i_log_test.get_logs(cid_file_name=cid_file_name)
        assert logs
        ContainerTestLibUtils.check_regexp_output(
            regexp_to_check="open.*failed.*No such file or directory",
            logs_to_check=logs
        )

    # test_log_volume_output
    def test_log_volume_output(self, s2i_log_test):
        cid_file_name = "test-app"
        s2i_log_test.set_new_image(image_name=f"{IMAGE_NAME}-{cid_file_name}")
        assert s2i_log_test.create_container(
            cid_file_name=cid_file_name,
            container_args=f"-e NGINX_LOG_TO_VOLUME=y --user 10001"
        )
        cid = s2i_log_test.get_cid(cid_file_name=cid_file_name)
        assert cid
        cip = s2i_log_test.get_cip(cid_file_name=cid_file_name)
        assert s2i_log_test.test_response(url=f"http://{cip}", port=8080, expected_output="NGINX is working")
        assert '"GET / HTTP/1.1" 200' in PodmanCLIWrapper.podman_get_file_content(
            cid_file_name=cid,
            filename="/var/log/nginx/access.log"
        )
        assert s2i_log_test.test_response(
            url=f"http://{cip}", port=8080, page="/nothing-at-all", expected_code=404
        )
        assert '"GET /nothing-at-all HTTP/1.1" 404' in PodmanCLIWrapper.podman_get_file_content(
            cid_file_name=cid,
            filename="/var/log/nginx/access.log"
        )
        assert ContainerTestLibUtils.check_regexp_output(
            regexp_to_check="open.*failed.*No such file or directory",
            logs_to_check=PodmanCLIWrapper.podman_get_file_content(
                cid_file_name=cid,
                filename="/var/log/nginx/error.log"
            )
        )
