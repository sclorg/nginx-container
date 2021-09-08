# Test application for Nginx

This is a simple example of static content and configuration files served using nginx.

## Building with s2i and Dockerfile

See [the main documentation](/1.18/README.md) for steps how to use this image
with a podman directly or in a Dockerfile, utilizing the source-to-image scripts.

## Building and deploying in OpenShift

### Version 1.16
```
oc new-app nginx:1.16~https://github.com/sclorg/nginx-container.git --context-dir=1.16/test/test-app/
```
### Version 1.18
```
oc new-app nginx:1.18~https://github.com/sclorg/nginx-container.git --context-dir=1.18/test/test-app/
```
