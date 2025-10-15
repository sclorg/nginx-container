from container_ci_suite.helm import HelmChartsAPI

from conftest import VARS, TAGS


class TestHelmNginxTemplate:

    def setup_method(self):
        package_name = "redhat-nginx-template"
        self.hc_api = HelmChartsAPI(
            path=VARS.TEST_DIR, package_name=package_name, tarball_dir=VARS.TEST_DIR, shared_cluster=True
        )
        self.hc_api.clone_helm_chart_repo(
            repo_url="https://github.com/sclorg/helm-charts", repo_name="helm-charts",
            subdir="charts/redhat"
        )

    def teardown_method(self):
        self.hc_api.delete_project()

    def test_helm_connection(self):
        """
        Test checks if Helm imagestream and Helm nginx template application
        works properly and response is as expected.
        """
        self.hc_api.package_name = "redhat-nginx-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "redhat-nginx-template"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "nginx_version": f"{VARS.VERSION_NO_MICRO}{TAGS.get(VARS.OS)}",
                "namespace": self.hc_api.namespace
            }
        )
        expected_str = "Welcome to your static nginx application on OpenShift"
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix="nginx-example")
        assert self.hc_api.test_helm_chart(expected_str=[expected_str])
