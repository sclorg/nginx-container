import pytest

from container_ci_suite.container_lib import ContainerTestLib
from container_ci_suite.engines.podman_wrapper import PodmanCLIWrapper
from container_ci_suite.dockerfile_processor import DockerfileProcessor

from conftest import VARS


class TestNginxContainer:

    def setup_method(self):
        self.app = ContainerTestLib(image_name=VARS.IMAGE_NAME, s2i_image=True)

    def teardown_method(self):
        self.app.cleanup()

    def test_run_s2i_usage(self):
        """
        Test if s2i usage works
        """
        output = self.app.s2i_usage()
        assert output != ""

    def test_docker_run_usage(self):
        """
        Test if container is runnable
        """
        assert PodmanCLIWrapper.call_podman_command(
            cmd=f"run --rm {VARS.IMAGE_NAME} &>/dev/null",
            return_output=False
        ) == 0

    def test_scl_usage(self):
        """
        Test if nginx -v returns proper output
        """

        assert f"nginx/{VARS.VERSION_NO_MICRO}" in PodmanCLIWrapper.podman_run_command_and_remove(
            cid_file_name=VARS.IMAGE_NAME,
            cmd="nginx -v"
        )

    @pytest.mark.parametrize(
        "dockerfile",
        [
            "Dockerfile",
            "Dockerfile.s2i"
        ]
    )
    def test_dockerfiles(self, dockerfile):
        """
        Test if building nginx-container based on
        examples/Dockerfile works
        """
        dp = DockerfileProcessor(dockerfile_path=f"{VARS.TEST_DIR}/examples/{dockerfile}")
        dp.update_env_in_dockerfile(version=VARS.VERSION_NO_MICRO, what_to_replace="ENV NGINX_VERSION")
        dp.update_variable_in_dockerfile(version=VARS.VERSION_NO_MICRO, variable="NGINX_VERSION")
        new_docker_file = dp.create_temp_dockerfile()

        assert self.app.build_test_container(
            dockerfile=new_docker_file, app_url="https://github.com/sclorg/nginx-container.git",
            app_dir="nginx-container"
        )
        assert self.app.test_app_dockerfile()
        cip = self.app.get_cip()
        assert cip
        assert self.app.test_response(url=cip, expected_output="NGINX is working")
