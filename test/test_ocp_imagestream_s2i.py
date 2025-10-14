from container_ci_suite.openshift import OpenShiftAPI
from container_ci_suite.utils import get_service_image

from conftest import VARS

# bash test=test_nginx_imagestream
class TestNginxImagestreamS2I:

    def setup_method(self):
        self.template_name = get_service_image(VARS.IMAGE_NAME)
        self.oc_api = OpenShiftAPI(
            pod_name_prefix=self.template_name, version=VARS.VERSION, shared_cluster=True
        )

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_inside_cluster(self):
        os_name = ''.join(i for i in VARS.OS if not i.isdigit())
        assert self.oc_api.deploy_imagestream_s2i(
            imagestream_file=f"imagestreams/nginx-{os_name}.json",
            image_name=VARS.IMAGE_NAME,
            app="https://github.com/sclorg/nginx-container.git",
            context=f"examples/{VARS.VERSION_NO_MICRO}/test-app",
            service_name=self.template_name
        )
        assert self.oc_api.is_template_deployed(name_in_template=self.template_name)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=self.template_name, expected_output="Test NGINX passed"
        )
