import os
import sys
import pytest

from pathlib import Path

from container_ci_suite.container_lib import ContainerTestLib
from container_ci_suite.engines.podman_wrapper import PodmanCLIWrapper
from container_ci_suite.utils import check_variables, ContainerTestLibUtils
from container_ci_suite.engines.container import ContainerImage

if not check_variables():
    print("At least one variable from OS, VERSION is missing.")
    sys.exit(1)

TEST_DIR = Path(os.path.abspath(os.path.dirname(__file__)))

VERSION = os.getenv("VERSION")
OS = os.getenv("TARGET")

IMAGE_NAME = os.getenv("IMAGE_NAME")
if not IMAGE_NAME:
    print(f"Built container for version {VERSION} on OS {OS} does not exist.")
    sys.exit(1)

image_tag_wo_tag = IMAGE_NAME.split(":")[0]
image_tag = IMAGE_NAME.split(":")[1]
perl_test_app = os.path.join(TEST_DIR, "perl-test-app")
start_hook_test_app = os.path.join(TEST_DIR, "start-hook-test-app")

app_params_perl_test_app = [perl_test_app]
app_params_start_hook = [start_hook_test_app]


@pytest.fixture(scope="module", params=app_params_start_hook)
def example_app_test(request):
    container_lib = ContainerTestLib(IMAGE_NAME)
    app_name = os.path.basename(request.param)
    print(f"App Name: {app_name}")
    s2i_app = container_lib.build_as_df(
        app_path=request.param,
        s2i_args="--pull-policy=never",
        src_image=IMAGE_NAME,
        dst_image=f"{IMAGE_NAME}-{app_name}"
    )
    s2i_app.set_new_image(image_name=f"{IMAGE_NAME}-{app_name}")
    yield s2i_app
    s2i_app.clean_containers()

@pytest.fixture(scope="module", params=app_params_perl_test_app)
def example_perl_test(request):
    container_lib = ContainerTestLib(IMAGE_NAME)
    app_name = os.path.basename(request.param)
    print(f"App Name: {app_name}")
    s2i_app = container_lib.build_as_df(
        app_path=request.param,
        s2i_args="--pull-policy=never",
        src_image=IMAGE_NAME,
        dst_image=f"{IMAGE_NAME}-{app_name}"
    )
    s2i_app.set_new_image(image_name=f"{IMAGE_NAME}-{app_name}")
    yield s2i_app
    s2i_app.clean_containers()

@pytest.mark.usefixtures("example_app_test")
class TestNginxExampleAppContainer:

    def test_run_app_test(self, example_app_test):
        version = VERSION.replace("-micro", "")
        cid_file = example_app_test.app_name
        assert example_app_test.create_container(cid_file=cid_file, container_args="--user 10001")
        assert ContainerImage.wait_for_cid(cid_file=cid_file)
        cid = example_app_test.get_cid(cid_name=cid_file)
        assert cid
        cip = example_app_test.get_cip(cid_name=cid_file)
        assert cip
        command = PodmanCLIWrapper.podman_get_file_content(cid_name=cid, filename="/opt/app-root/etc/nginx.d/default.conf")
        print(f"Content of default.conf is {command}")
        assert ContainerTestLibUtils.check_regexp_output(regexp_to_check="resolver", logs_to_check=command)
        assert not ContainerTestLibUtils.check_regexp_output(regexp_to_check="DNS_SERVER", logs_to_check=command)
        assert PodmanCLIWrapper.podman_run_command(
            f"--rm {example_app_test.image_name} /bin/bash -c 'nginx -v'"
        ).startswith(f"nginx version: nginx/{version}")
        assert example_app_test.test_response(
            url=f"http://{cip}", expected_output="NGINX is working"
        )
        assert example_app_test.test_response(
            url=f"http://{cip}", expected_output="NGINX2 is working",
            host="localhost2"
        )
        assert example_app_test.test_response(
            url=f"http://{cip}", expected_code=404,
            page="/nginx-cfg/default.conf"
        )

@pytest.mark.usefixtures("example_perl_test")
class TestNginxExamplePerlAppContainer:

    def test_run_app_test(self, example_perl_test):
        if VERSION.endswith("-micro"):
            pytest.skip("Run the chosen tests (not for micro variant which lacks perl)")
        cid_file = example_perl_test.app_name
        example_perl_test.set_new_image(image_name=f"{IMAGE_NAME}-{cid_file}")
        assert example_perl_test.create_container(cid_file=cid_file, container_args="--user 10001")
        cid = example_perl_test.get_cid(cid_name=cid_file)
        assert cid
        cip = example_perl_test.get_cip(cid_name=cid_file)
        assert cip
        print(f"CIP: {cip}")
        perl_version = PodmanCLIWrapper.podman_exec_bash_command(cid_name=cid, cmd="perl -e 'print \"$^V\"'")
        print(f"Content of perl is: '{perl_version}'.")
        assert example_perl_test.test_response(
            url=f"http://{cip}", port=8080,
            expected_output=f"X-Perl-Version: {perl_version}"
        )
        assert example_perl_test.test_response(
            url=f"http://{cip}", port=8080, page="/perl", expected_output="Perl location handler is working"
        )

