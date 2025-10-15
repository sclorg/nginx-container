from container_ci_suite.openshift import OpenShiftAPI
from conftest import VARS


class TestNginxDeployTemplate:

    def setup_method(self):
        self.oc_api = OpenShiftAPI(pod_name_prefix="nginx-testing", version=VARS.VERSION, shared_cluster=True)

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_nginx_template_inside_cluster(self):
        """
        Test checks if Helm imagestream and Helm perl dancer application
        works properly and response is as expected.
        """
        service_name = "nginx-testing"
        template_url = self.oc_api.get_raw_url_for_json(
            container="nginx-ex", dir="openshift/templates", filename="nginx.json", branch="master"
        )
        assert self.oc_api.deploy_template_with_image(
            image_name=VARS.IMAGE_NAME,
            template=template_url,
            name_in_template="nginx",
            openshift_args=[
                "SOURCE_REPOSITORY_REF=master",
                f"NGINX_VERSION={VARS.VERSION}",
                f"NAME={service_name}"
            ]
        )
        assert self.oc_api.is_template_deployed(name_in_template=service_name, timeout=300)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name, expected_output="Welcome to your static nginx application on OpenShift"
        )
