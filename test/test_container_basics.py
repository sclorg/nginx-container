import pytest

from container_ci_suite.container_lib import ContainerTestLib
from container_ci_suite.engines.podman_wrapper import PodmanCLIWrapper
from container_ci_suite.dockerfile_processor import DockerfileProcessor

from constants import TEST_DIR, IMAGE_NAME, VERSION


class TestNginxContainer:

    def setup_method(self):
        self.app = ContainerTestLib(image_name=IMAGE_NAME, s2i_image=True)

    def teardown_method(self):
        self.app.cleanup()

    def test_run_s2i_usage(self, app):
        """
        Test if s2i usage works
        """
        output = app.s2i_usage()
        assert output != ""

    def test_docker_run_usage(self):
        """
        Test if container is runnable
        """
        assert PodmanCLIWrapper.call_podman_command(
            cmd=f"run --rm {IMAGE_NAME} &>/dev/null",
            return_output=False
        ) == 0

    def test_scl_usage(self):
        """
        Test if nginx -v returns proper output
        """
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
        """
        Test if building nginx-container based on
        examples/Dockerfile works
        """
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
        assert app.test_response(url=cip, expected_output="NGINX is working")
