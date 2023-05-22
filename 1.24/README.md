Nginx 1.24 server and a reverse proxy server container image
============================================================
This container image includes Nginx 1.24 server and a reverse server for OpenShift and general usage.
Users can choose between RHEL, CentOS, CentOS Stream and Fedora based images.
The RHEL images are available in the [Red Hat Container Catalog](https://access.redhat.com/containers/),
the CentOS Stream images are available in the [Quay.io](https://quay.io/organization/sclorg),
and the Fedora images are available in the [Quay.io](https://quay.io/organization/fedora).
The resulting image can be run using [podman](https://github.com/containers/libpod).

Note: while the examples in this README are calling `podman`, you can replace any such calls by `docker` with the same arguments.


Description
-----------

Nginx is a web server and a reverse proxy server for HTTP, SMTP, POP3 and IMAP
protocols, with a strong focus on high concurrency, performance and low memory usage. The container
image provides a containerized packaging of the nginx 1.24 daemon. The image can be used
as a base image for other applications based on nginx 1.24 web server.
Nginx server image can be extended using Openshift's `Source` build feature.


Usage in OpenShift
------------------
In this example, we assume that you are using the `ubi8/nginx-122` image, available through the `nginx:1.22` imagestream tag in Openshift.
To build a simple [test-app](https://github.com/sclorg/nginx-container/tree/master/examples/1.22/test-app) application in Openshift:

```
oc new-app nginx:1.22~https://github.com/sclorg/nginx-container.git --context-dir=1.22/test/test-app/
```

To access the application:
```
$ oc get pods
$ oc exec <pod> -- curl 127.0.0.1:8080
```


Source-to-Image framework and scripts
-------------------------------------
This image supports the [Source-to-Image](https://docs.openshift.com/container-platform/4.4/builds/build-strategies.html#images-create-s2i_build-strategies)
(S2I) strategy in OpenShift. The Source-to-Image is an OpenShift framework
which makes it easy to write images that take application source code as
an input, use a builder image like this Nginx container image, and produce
a new image that runs the assembled application as an output.

In case of Nginx container image, the application source code is typically
either static HTML pages or configuration files.

To support the Source-to-Image framework, important scripts are included in the builder image:

* The `/usr/libexec/s2i/run` script is set as the default command in the resulting container image (the new image with the application artifacts).

* The `/usr/libexec/s2i/assemble` script inside the image is run to produce a new image with the application artifacts. The script takes sources of a given application (HTML pages), Nginx configuration files, and places them into appropriate directories inside the image. The structure of nginx-app can look like this:

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


Build an application using a Dockerfile
---------------------------------------
Compared to the Source-to-Image strategy, using a Dockerfile is a more
flexible way to build an Nginx container image with an application.
Use a Dockerfile when Source-to-Image is not sufficiently flexible for you or
when you build the image outside of the OpenShift environment.

To use the Nginx image in a Dockerfile, follow these steps:

#### 1. Pull a base builder image to build on

podman pull ubi8/nginx-122

#### 2. Pull an application code

An example application available at https://github.com/sclorg/nginx-container.git is used here. To adjust the example application, clone the repository.

```
git clone https://github.com/sclorg/nginx-container.git nginx-container
cd nginx-container/examples/1.22/
```

#### 3. Prepare an application inside a container

This step usually consists of at least these parts:

* putting the application source into the container
* moving configuration files to the correct place (if available in the application source code)
* setting the default command in the resulting image

For all these three parts, you can either set up all manually and use the `nginx` command explicitly in the Dockerfile ([3.1.](#31-to-use-own-setup-create-a-dockerfile-with-this-content)), or you can use the Source-to-Image scripts inside the image ([3.2.](#32-to-use-the-source-to-image-scripts-and-build-an-image-using-a-dockerfile-create-a-dockerfile-with-this-content); see more about these scripts in the section "Source-to-Image framework and scripts" above), that already know how to set-up and run some common Nginx applications.

##### 3.1. To use your own setup, create a Dockerfile with this content:

```
FROM registry.access.redhat.com/ubi8/nginx-122

# Add application sources
ADD test-app/nginx.conf "${NGINX_CONF_PATH}"
ADD test-app/nginx-default-cfg/*.conf "${NGINX_DEFAULT_CONF_PATH}"
ADD test-app/nginx-cfg/*.conf "${NGINX_CONFIGURATION_PATH}"
ADD test-app/*.html .

# Run script uses standard ways to run the application
CMD nginx -g "daemon off;"
```

##### 3.2. To use the Source-to-Image scripts and build an image using a Dockerfile, create a Dockerfile with this content:

```
FROM registry.access.redhat.com/ubi8/nginx-122

# Add application sources to a directory where the assemble script expects them
# and set permissions so that the container runs without root access
# With older docker that does not support --chown option for ADD statement,
# use these statements instead:
#  USER 0
#  ADD app-src /tmp/src
#  RUN chown -R 1001:0 /tmp/src
#  USER 1001
ADD --chown=1001:0 app-src /tmp/src

# Let the assemble script to install the dependencies
RUN /usr/libexec/s2i/assemble

# Run script uses standard ways to run the application
CMD /usr/libexec/s2i/run
```

#### 4. Build a new image from a Dockerfile prepared in the previous step
```
podman build -t nginx-app .
```

#### 5. Run the resulting image with the final application
```
podman run -d nginx-app
```


Direct usage with a mounted directory
-------------------------------------
An example of the data on the host for the following example:
```
$ ls -lZ /wwwdata/html
-rw-r--r--. 1 1001 1001 54321 Jan 01 12:34 index.html
-rw-r--r--. 1 1001 1001  5678 Jan 01 12:34 page.html
```

If you want to run the image directly and mount the static pages available in the `/wwwdata/` directory on the host
as a container volume, execute the following command:

```
$ podman run -d --name nginx -p 8080:8080 -v /wwwdata:/opt/app-root/src:Z ubi8/nginx-122 nginx -g "daemon off;"
```

This creates a container named `nginx` running the Nginx server, serving data from
the `/wwwdata/` directory. Port 8080 is exposed and mapped to the host.
You can pull the data from the nginx container using this command:

```
$ curl -Lk 127.0.0.1:8080
```

You can replace `/wwwdata/` with location of your web root. Please note that this has to be an **absolute** path, due to podman requirements.


Environment variables and volumes
---------------------------------
The nginx container image supports the following configuration variable, which can be set by using the `-e` option with the podman run command:


**`NGINX_LOG_TO_VOLUME`**
       When `NGINX_LOG_TO_VOLUME` is set, nginx logs into `/var/log/nginx/`.


Troubleshooting
---------------
By default, nginx access logs are written to standard output and error logs are written to standard error, so both are available in the container log. The log can be examined by running:

    podman logs <container>

See also
--------
Dockerfile and other sources for this container image are available on
https://github.com/sclorg/nginx-container.
In that repository you also can find another versions of Python environment Dockerfiles.
for RHEL8 it's `Dockerfile.rhel8`, Dockerfile for CentOS Stream 8 is called `Dockerfile.c8s`,
Dockerfile for CentOS Stream 9 is called `Dockerfile.c9s` and the Fedora Dockerfile is called `Dockerfile.fedora`.

