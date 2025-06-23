import os
import sys
import pytest

from container_ci_suite.openshift import OpenShiftAPI
from container_ci_suite.utils import get_service_image, check_variables

if not check_variables():
    print("At least one variable from IMAGE_NAME, OS, VERSION is missing.")
    sys.exit(1)

VERSION = os.getenv("VERSION")
IMAGE_NAME = os.getenv("IMAGE_NAME")
OS = os.getenv("TARGET")


# Replacement with 'test_python_s2i_app_ex_standalone'
class TestNginxLocalEx:

    def setup_method(self):
        self.template_name = get_service_image(IMAGE_NAME)
        self.oc_api = OpenShiftAPI(pod_name_prefix=self.template_name, version=VERSION, shared_cluster=True)

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_nginx_ex_template_inside_cluster(self):
        assert self.oc_api.deploy_s2i_app(
            image_name=IMAGE_NAME, app="test-app",
            context=".",
            service_name=self.template_name
        )
        assert self.oc_api.is_template_deployed(name_in_template=self.template_name)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=self.template_name, expected_output="Test NGINX passed"
        )
