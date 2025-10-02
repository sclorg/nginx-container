import os
import sys
import pytest


from pathlib import Path
from container_ci_suite.container_lib import ContainerTestLib
from container_ci_suite.engines.podman_wrapper import PodmanCLIWrapper
from container_ci_suite.utils import check_variables


TEST_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
if not check_variables():
    print("At least one variable from IMAGE_NAME, OS, VERSION is missing.")
    sys.exit(1)
VERSION = os.getenv("VERSION")
IMAGE_NAME = os.getenv("IMAGE_NAME")
OS = os.getenv("TARGET").lower()
test_app = os.path.join(TEST_DIR, "test-app")


@pytest.fixture(scope="module", params=[test_app])
def app(request):
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


class TestNginxApplicationContainer:

    # test_application
    def test_application(self, app):
        version = VERSION.replace("-micro", "")
        cid_file_name = "test-app"
        app.set_new_image(image_name=f"{IMAGE_NAME}-{cid_file_name}")
        assert app.create_container(
            cid_file_name=cid_file_name,
            container_args=f"--user 10001"
        )
        cip = app.get_cip(cid_file_name=cid_file_name)
        assert PodmanCLIWrapper.podman_run_command(
            f"--rm {app.image_name} /bin/bash -c 'nginx -v'"
        ).startswith(f"nginx version: nginx/{version}")
        assert app.test_response(
            url=f"http://{cip}", expected_output="NGINX is working"
        )
        assert app.test_response(
            url=f"http://{cip}", expected_output="NGINX2 is working",
            host="localhost2"
        )
        assert app.test_response(
            url=f"http://{cip}", expected_output="NGINX2 is working",
            page="/aliased/index2.html"
        )
        assert app.test_response(
            url=f"http://{cip}", expected_code=404,
            page="/nginx-cfg/default.conf"
        )


    # test_application_user
    def test_application_user(self, app):
        version = VERSION.replace("-micro", "")
        cid_file_name = "test-app"
        app.set_new_image(image_name=f"{IMAGE_NAME}-{cid_file_name}")
        assert app.create_container(
            cid_file_name=cid_file_name,
            container_args=f"--user 10001 --user 12345"
        )
        cip = app.get_cip(cid_file_name=cid_file_name)
        assert PodmanCLIWrapper.podman_run_command(
            f"--rm {app.image_name} /bin/bash -c 'nginx -v'"
        ).startswith(f"nginx version: nginx/{version}")
        assert app.test_response(
            url=f"http://{cip}", expected_output="NGINX is working"
        )
        assert app.test_response(
            url=f"http://{cip}", expected_output="NGINX2 is working",
            host="localhost2"
        )
        assert app.test_response(
            url=f"http://{cip}", expected_output="NGINX2 is working",
            page="/aliased/index2.html"
        )
        assert app.test_response(
            url=f"http://{cip}", expected_code=404,
            page="/nginx-cfg/default.conf"
        )
