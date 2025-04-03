import os
import sys
import pytest

from pathlib import Path

from container_ci_suite.openshift import OpenShiftAPI
from container_ci_suite.utils import get_service_image, check_variables

if not check_variables():
    print("At least one variable from IMAGE_NAME, OS, VERSION is missing.")
    sys.exit(1)


VERSION = os.getenv("VERSION")
IMAGE_NAME = os.getenv("IMAGE_NAME")
OS = os.getenv("TARGET")


# bash test_nginx_template_from_example_app
# Replacement with 'test_python_s2i_templates'
class TestNginxDeployTemplate:

    def setup_method(self):
        self.oc_api = OpenShiftAPI(pod_name_prefix="nginx-testing", version=VERSION)

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_nginx_template_inside_cluster(self):
        if OS == "rhel10":
            pytest.skip("Skipping test for rhel10")
        service_name = "nginx-testing"
        template_url = self.oc_api.get_raw_url_for_json(
            container="nginx-ex", dir="openshift/templates", filename="nginx.json", branch="master"
        )
        assert self.oc_api.deploy_template_with_image(
            image_name=IMAGE_NAME,
            template=template_url,
            name_in_template="nginx",
            openshift_args=[
                f"SOURCE_REPOSITORY_REF=master",
                f"NGINX_VERSION={VERSION}",
                f"NAME={service_name}"
            ]
        )
        assert self.oc_api.is_template_deployed(name_in_template=service_name, timeout=300)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name, expected_output="Welcome to your static nginx application on OpenShift"
        )
