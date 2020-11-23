Nginx 1.18 server and a reverse proxy server container image
============================================================
This container image includes Nginx 1.18 server and a reverse server for OpenShift and general usage.
Users can choose between RHEL, CentOS and Fedora based images.
The RHEL images are available in the [Red Hat Container Catalog](https://access.redhat.com/containers/),
the CentOS images are available on [Quay.io](https://quay.io/organization/centos7),
and the Fedora images are available in [Fedora Registry](https://registry.fedoraproject.org/).
The resulting image can be run using [podman](https://github.com/containers/libpod).

Note: while the examples in this README are calling `podman`, you can replace any such calls by `docker` with the same arguments.

Description
-----------

Nginx is a web server and a reverse proxy server for HTTP, SMTP, POP3 and IMAP
protocols, with a strong focus on high concurrency, performance and low memory usage. The container
image provides a containerized packaging of the nginx 1.18 daemon. The image can be used
as a base image for other applications based on nginx 1.18 web server.
Nginx server image can be extended using Openshift's `Source` build feature.


Usage
-----

For this, we will assume that you are using the `rhel8/nginx-118` image, available via `nginx:1.18` imagestream tag in Openshift.
Building a simple [sample-app](https://github.com/sclorg/nginx-container/tree/master/1.18/test/test-app) application
in Openshift can be achieved with the following step:

    ```
    oc new-app nginx:1.18~https://github.com/sclorg/nginx-container.git --context-dir=1.18/test/test-app/
    ```

The same application can also be built using the standalone [S2I](https://github.com/openshift/source-to-image) application on systems that have it available:

    ```
    $ s2i build https://github.com/sclorg/nginx-container.git --context-dir=1.18/test/test-app/ rhel8/nginx-118 nginx-sample-app
    ```

**Accessing the application:**
```
$ curl 127.0.0.1:8080
```


S2I build support
-----------------
This image can be extended in Openshift using the `Source` build strategy or via the standalone
[source-to-image](https://github.com/openshift/source-to-image) application (where available).
S2I build folder structure:

**`./nginx.conf`**--
       The main nginx configuration file

**`./nginx-cfg/*.conf`**
       Should contain all nginx configuration we want to include into image

**`./nginx-default-cfg/*.conf`**
       Contains any nginx config snippets to include in the default server block

**`./nginx-start/*.sh`**
       Contains shell scripts that are sourced right before nginx is launched

**`./nginx-perl/*.pm`**
       Contains perl modules to be use by `perl_modules` and `perl_require` directives

**`./`**
       Should contain nginx application source code


Environment variables and volumes
---------------------------------
The nginx container image supports the following configuration variable, which can be set by using the `-e` option with the podman run command:


**`NGINX_LOG_TO_VOLUME`**
       When `NGINX_LOG_TO_VOLUME` is set, nginx logs into `/var/log/nginx/`. In case of RHEL-7 and CentOS-7 images, this is a symlink to `/var/opt/rh/rh-nginx118/log/nginx/`.


You can mount your own web root like this:
```
$ podman run -v <DIR>:/var/www/html/ <container>
```
You can replace \<DIR> with location of your web root. Please note that this has to be an **absolute** path, due to podman requirements.


Troubleshooting
---------------
By default, nginx access logs are written to standard output and error logs are written to standard error, so both are available in the container log. The log can be examined by running:

    podman logs <container>

**If `NGINX_LOG_TO_VOLUME` variable is set, nginx logs into `/var/log/nginx/`. In case of RHEL-7 and CentOS-7 images, this is a symlink to `/var/opt/rh/rh-nginx118/log/nginx/`, which can be mounted to host system using the container volumes.**


See also
--------
Dockerfile and other sources for this container image are available on
https://github.com/sclorg/nginx-container.
In that repository you also can find another versions of Python environment Dockerfiles.
Dockerfile for CentOS is called `Dockerfile`, Dockerfile for RHEL7 is called `Dockerfile.rhel7`,
for RHEL8 it's `Dockerfile.rhel8` and the Fedora Dockerfile is called Dockerfile.fedora.

