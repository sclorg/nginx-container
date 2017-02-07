# Variables are documented in hack/build.sh.
BASE_IMAGE_NAME = nginx
VERSIONS = 1.6 1.8 1.10
OPENSHIFT_NAMESPACES = 

# Include common Makefile code.
include hack/common.mk
