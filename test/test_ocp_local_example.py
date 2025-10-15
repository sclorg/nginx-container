from container_ci_suite.openshift import OpenShiftAPI
from container_ci_suite.utils import get_service_image

from conftest import VARS


class TestNginxLocalEx:

    def setup_method(self):
        self.template_name = get_service_image(VARS.IMAGE_NAME)
        self.oc_api = OpenShiftAPI(
            pod_name_prefix=self.template_name, version=VARS.VERSION, shared_cluster=True
        )

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_nginx_ex_template_inside_cluster(self):
        """
        Test checks if example nginx container
        works with local test-app
        The example application is in directory `examples/<VERSION>/test-app
        """
        assert self.oc_api.deploy_s2i_app(
            image_name=VARS.IMAGE_NAME, app="test-app",
            context=".",
            service_name=self.template_name
        )
        assert self.oc_api.is_template_deployed(name_in_template=self.template_name)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=self.template_name, expected_output="Test NGINX passed"
        )
