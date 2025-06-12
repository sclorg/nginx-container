#!/bin/bash
#
# Functions for tests for the nginx image in OpenShift.
#
# IMAGE_NAME specifies a name of the candidate image used for testing.
# The image has to be available before this script is executed.
#

THISDIR=$(dirname ${BASH_SOURCE[0]})

source "${THISDIR}/test-lib.sh"
source "${THISDIR}/test-lib-openshift.sh"

function test_nginx_integration() {
  ct_os_test_s2i_app "${IMAGE_NAME}" \
                     "https://github.com/sclorg/nginx-container.git" \
                     "examples/${VERSION}/test-app" \
                     "Test NGINX passed"
}

# Check the imagestream
function test_nginx_imagestream() {
  # Check if the current version is already GA
  # This directory is cloned from TMT plan repo 'sclorg-tmt-plans'
  local devel_file="/root/sclorg-tmt-plans/devel_images"
  if [ -f "${devel_file}" ]; then
    if grep -q "${OS}=nginx-container=${VERSION}" "$devel_file" ; then
      echo "This version is currently developed, so skipping this test."
      return
    fi
  fi
  ct_os_test_image_stream_s2i "${THISDIR}/imagestreams/nginx-${OS//[0-9]/}.json" "${IMAGE_NAME}" \
                              "https://github.com/sclorg/nginx-container.git" \
                              "examples/${VERSION}/test-app" \
                              "Test NGINX passed"
}

function test_nginx_local_example() {
  # test local app
  ct_os_test_s2i_app ${IMAGE_NAME} "${THISDIR}/test-app" . 'Test NGINX passed'
}

function test_nginx_remote_example() {
  # TODO: branch should be changed to master, once code in example app
  # stabilizes on with referencing latest version
  BRANCH_TO_TEST=master
  # test remote example app
  ct_os_test_s2i_app "${IMAGE_NAME}" \
                     "https://github.com/sclorg/nginx-ex.git#${BRANCH_TO_TEST}" \
                     . \
                     'Welcome to your static nginx application on OpenShift'
}

function test_nginx_template_from_example_app() {
  BRANCH_TO_TEST=master
  # test template from the example app
  ct_os_test_template_app "${IMAGE_NAME}" \
                          "https://raw.githubusercontent.com/sclorg/nginx-ex/${BRANCH_TO_TEST}/openshift/templates/nginx.json" \
                          nginx \
                          'Welcome to your static nginx application on OpenShift' \
                          8080 http 200 "-p SOURCE_REPOSITORY_REF=${BRANCH_TO_TEST} -p NGINX_VERSION=${VERSION} -p NAME=nginx-testing"

}

function test_latest_imagestreams() {
  local result=1
  if [[ "${VERSION}" == *"micro"* ]]; then
    echo "Do not check 'micro' imagestreams. Only main versions."
    return 0
  fi
    if [[ "${OS}" == "rhel8" ]]; then
    echo "Do not check the latest version in imagestreams for RHEL8. It does not contain the latest version."
    return 0
  fi
  echo "Testing the latest version in imagestreams"
  pushd "${THISDIR}/../.." >/dev/null || return 1
  ct_check_latest_imagestreams
  result=$?
  popd >/dev/null || return 1
  return $result
}

# vim: set tabstop=2:shiftwidth=2:expandtab:
