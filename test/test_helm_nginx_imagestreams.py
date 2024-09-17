import os
import sys

import pytest

from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI
from container_ci_suite.utils import check_variables

if not check_variables():
    print("At least one variable from IMAGE_NAME, OS, VERSION is missing.")
    sys.exit(1)

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmRHELNginxImageStreams:

    def setup_method(self):
        package_name = "nginx-imagestreams"
        path = test_dir
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir, remote=True)
        self.hc_api.clone_helm_chart_repo(
            repo_url="https://github.com/sclorg/helm-charts", repo_name="helm-charts",
            subdir="charts/redhat"
        )

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,registry",
        [
            ("1.24-ubi9", "registry.redhat.io/ubi9/nginx-124:latest"),
            ("1.24-ubi8", "registry.redhat.io/ubi8/nginx-124:latest"),
            ("1.22-ubi9", "registry.redhat.io/ubi9/nginx-122:latest"),
            ("1.22-ubi8", "registry.redhat.io/ubi8/nginx-122:latest"),
            ("1.20-ubi9", "registry.redhat.io/ubi9/nginx-120:latest"),
            ("1.20-ubi8", "registry.redhat.io/ubi8/nginx-120:latest"),
        ],
    )
    def test_package_imagestream(self, version, registry):
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        assert self.hc_api.check_imagestreams(version=version, registry=registry)
