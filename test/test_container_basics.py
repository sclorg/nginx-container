import os
import sys
import pytest

from pathlib import Path
from container_ci_suite.container_lib import ContainerTestLib
from container_ci_suite.engines.podman_wrapper import PodmanCLIWrapper
from container_ci_suite.utils import check_variables, ContainerTestLibUtils
from container_ci_suite.dockerfile_processor import DockerfileProcessor
from container_ci_suite.git import Git

TEST_DIR = Path(os.path.abspath(os.path.dirname(__file__)))

if not check_variables():
    print("At least one variable from IMAGE_NAME, OS, VERSION is missing.")
    sys.exit(1)

VERSION = os.getenv("VERSION", None)
IMAGE_NAME = os.getenv("IMAGE_NAME", None)
OS = os.getenv("TARGET", None)


image_name = IMAGE_NAME.split(":")[0]
image_tag = IMAGE_NAME.split(":")[1]
test_dir = os.path.join(os.getcwd())
print(f"Test dir is: {TEST_DIR}")


@pytest.fixture(scope="module")
def app(request):
    app = ContainerTestLib(image_name=IMAGE_NAME, s2i_image=True)
    # app_name = os.path.basename(request.param)
    yield app
    app.clean_containers()
    app.clean_app_images()

class TestNginxContainer:

        # test_s2i_usage
        def test_run_s2i_usage(self, app):
            output = app.s2i_usage()
            print(f"S2i_USAGE output: '{output}'")
            assert output != ""

        # # test_docker_run_usage
        def test_docker_run_usage(self):
            assert PodmanCLIWrapper.call_podman_command(
                cmd=f"run --rm {IMAGE_NAME} &>/dev/null",
                return_output=False
            ) == 0


        def test_scl_usage(self):
            version = VERSION.replace("-micro", "")
            assert PodmanCLIWrapper.podman_run_command(
                f"--rm {IMAGE_NAME} /bin/bash -c 'nginx -v'"
            ).startswith(f"nginx version: nginx/{version}")

        @pytest.mark.parametrize(
            "dockerfile",
            [
                "Dockerfile",
                "Dockerfile.s2i"
            ]
        )
        def test_dockerfiles(self, app, dockerfile):
            version = VERSION.replace("-micro", "")
            dp = DockerfileProcessor(dockerfile_path=f"{TEST_DIR}/examples/{dockerfile}")
            dp.update_env_in_dockerfile(version=version, what_to_replace="ENV NGINX_VERSION")
            dp.update_variable_in_dockerfile(version=version, variable="NGINX_VERSION")
            new_docker_file = dp.create_temp_dockerfile()

            assert app.build_test_container(
                dockerfile=new_docker_file, app_url="https://github.com/sclorg/nginx-container.git",
                app_dir="nginx-container"
            )
            assert app.test_app_dockerfile()
            cip = app.get_cip()
            assert cip
            assert app.test_response(url=f"{cip}", expected_code=200,
                                     expected_output="NGINX is working")
