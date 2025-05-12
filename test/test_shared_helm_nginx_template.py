import os
import sys

import pytest

from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI
from container_ci_suite.utils import check_variables

from constants import TAGS

if not check_variables():
    print("At least one variable from IMAGE_NAME, OS, VERSION is missing.")
    sys.exit(1)

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


VERSION = os.getenv("VERSION")
IMAGE_NAME = os.getenv("IMAGE_NAME")
OS = os.getenv("TARGET")

TAG = TAGS.get(OS)


class TestHelmNginxTemplate:

    def setup_method(self):
        package_name = "redhat-nginx-template"
        path = test_dir
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir, shared_cluster=True)
        self.hc_api.clone_helm_chart_repo(
            repo_url="https://github.com/sclorg/helm-charts", repo_name="helm-charts",
            subdir="charts/redhat"
        )

    def teardown_method(self):
        self.hc_api.delete_project()

    def test_helm_connection(self):
        self.hc_api.package_name = "redhat-nginx-imagestreams"
        new_version = VERSION
        if "micro" in VERSION:
            new_version = VERSION.replace("-micro", "")
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "redhat-nginx-template"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "nginx_version": f"{new_version}{TAG}",
                "namespace": self.hc_api.namespace
            }
        )
        expected_str = "Welcome to your static nginx application on OpenShift"
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix="nginx-example")
        assert self.hc_api.test_helm_chart(expected_str=[expected_str])
