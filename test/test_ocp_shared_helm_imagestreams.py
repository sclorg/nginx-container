import pytest

from container_ci_suite.helm import HelmChartsAPI

from conftest import VARS


class TestHelmRHELNginxImageStreams:

    def setup_method(self):
        package_name = "redhat-nginx-imagestreams"
        self.hc_api = HelmChartsAPI(
            path=VARS.TEST_DIR, package_name=package_name, tarball_dir=VARS.TEST_DIR, shared_cluster=True
        )
        self.hc_api.clone_helm_chart_repo(
            repo_url="https://github.com/sclorg/helm-charts", repo_name="helm-charts",
            subdir="charts/redhat"
        )

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,registry,expected",
        [
            ("1.26-ubi10", "registry.redhat.io/ubi10/nginx-126:latest", True),
            ("1.26-ubi9", "registry.redhat.io/ubi9/nginx-126:latest", True),
            ("1.24-ubi9", "registry.redhat.io/ubi9/nginx-124:latest", True),
            ("1.24-ubi8", "registry.redhat.io/ubi8/nginx-124:latest", True),
            ("1.22-ubi9", "registry.redhat.io/ubi9/nginx-122:latest", True),
            ("1.22-ubi8", "registry.redhat.io/ubi8/nginx-122:latest", True),
            ("1.20-ubi9", "registry.redhat.io/ubi9/nginx-120:latest", True),
            ("1.20-ubi8", "registry.redhat.io/ubi8/nginx-120:latest", False),
        ],
    )
    def test_package_imagestream(self, version, registry, expected):
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        assert self.hc_api.check_imagestreams(version=version, registry=registry) == expected
