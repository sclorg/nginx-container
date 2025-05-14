import os
import sys
import pytest

from container_ci_suite.openshift import OpenShiftAPI
from container_ci_suite.utils import get_service_image, check_variables

from constants import BRANCH_TO_MASTER, TAGS
if not check_variables():
    print("At least one variable from IMAGE_NAME, OS, VERSION is missing.")
    sys.exit(1)

BRANCH_TO_TEST = BRANCH_TO_MASTER
IMAGE_NAME = os.getenv("IMAGE_NAME")
OS = os.getenv("OS")
VERSION = os.getenv("VERSION")

TAG = TAGS.get(OS)

# bash test=test_nginx_imagestream
class TestNginxImagestreamS2I:

    def setup_method(self):
        self.template_name = get_service_image(IMAGE_NAME)
        self.oc_api = OpenShiftAPI(pod_name_prefix=self.template_name, version=VERSION)

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_inside_cluster(self):
        os_name = ''.join(i for i in OS if not i.isdigit())
        new_version = VERSION
        if "-minimal" in VERSION:
            new_version = VERSION.replace("-minimal", "")
        assert self.oc_api.deploy_imagestream_s2i(
            imagestream_file=f"imagestreams/nginx-{os_name}.json",
            image_name=IMAGE_NAME,
            app="https://github.com/sclorg/nginx-container.git",
            context=f"examples/{new_version}/test-app",
            service_name=self.template_name
        )
        assert self.oc_api.is_template_deployed(name_in_template=self.template_name)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=self.template_name, expected_output="Test NGINX passed"
        )
