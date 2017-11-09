# `test-app`
This is a simple example of static content served using nginx.

## Building with s2i
### Version 1.8
```
s2i build https://github.com/sclorg/nginx-container.git --context-dir=examples/1.8/test/test-app/ centos/nginx-18-centos7 nginx-sample-app
```
### Version 1.10
```
s2i build https://github.com/sclorg/nginx-container.git --context-dir=examples/1.10/test/test-app/ centos/nginx-110-centos7 nginx-sample-app
```
### Version 1.12
```
s2i build https://github.com/sclorg/nginx-container.git --context-dir=examples/1.12/test/test-app/ centos/nginx-112-centos7 nginx-sample-app
```

## Building and deploying in OpenShift
### Version 1.8
```
oc new-app centos/nginx-18-centos7~https://github.com/sclorg/nginx-container.git --context-dir=examples/1.8/test/test-app/
```
### Version 1.10
```
oc new-app centos/nginx-110-centos7~https://github.com/sclorg/nginx-container.git --context-dir=examples/1.10/test/test-app/
```
### Version 1.12
```
oc new-app centos/nginx-112-centos7~https://github.com/sclorg/nginx-container.git --context-dir=examples/1.12/test/test-app/
```
