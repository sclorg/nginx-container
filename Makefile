# Variables are documented in common/build.sh.
BASE_IMAGE_NAME = nginx
VERSIONS = 1.20 1.22 1.22-micro 1.24 1.26
OPENSHIFT_NAMESPACES =
NOT_RELEASED_VERSIONS =
DOCKER_BUILD_CONTEXT = ..

# HACK:  Ensure that 'git pull' for old clones doesn't cause confusion.
# New clones should use '--recursive'.
.PHONY: $(shell test -f common/common.mk || echo >&2 'Please do "git submodule update --init" first.')

include common/common.mk

generate:
	for version in ${VERSIONS} ; do \
		if [[ "$$version" == *-micro ]]; then \
			$(generator) -v $$version -m manifest-micro.yml -s specs/multispec.yml ; \
		elif [[ "$$version" == *-minimal ]]; then \
			$(generator) -v $$version -m manifest-minimal.yml -s specs/multispec.yml ; \
		else \
			$(generator) -v $$version -m manifest.yml -s specs/multispec.yml ; \
		fi \
	done

# use clean-versions provided by common.mk
clean-hook: clean-versions

script_env += NOT_RELEASED_VERSIONS="$(NOT_RELEASED_VERSIONS)"
