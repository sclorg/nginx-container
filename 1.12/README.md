Nginx 1.12 server and a reverse proxy server Docker image
=========================================================

This container image includes Nginx 1.12 server and a reverse server for OpenShift and general usage.
Users can choose RHEL based image.
The RHEL image is available in the [Red Hat Container Catalog](https://access.redhat.com/containers/#/registry.access.redhat.com/rhscl/nginx-112-rhel7)
as registry.access.redhat.com/rhscl/nginx-112-rhel7.


Description
-----------

Nginx is a web server and a reverse proxy server for HTTP, SMTP, POP3 and IMAP 
protocols, with a strong focus on high concurrency, performance and low memory usage. The container 
image provides a containerized packaging of the nginx 1.12 daemon. The image can be used 
as a base image for other applications based on nginx 1.12 web server. 
Nginx server image can be extended using source-to-image tool.


Usage
-----

To build a simple [sample-app](https://github.com/sclorg/nginx-container/tree/master/1.12/test/test-app) application
using standalone [S2I](https://github.com/openshift/source-to-image) and then run the
resulting image with [Docker](http://docker.io) execute:

*  **For RHEL based image**
    ```
    $ s2i build https://github.com/sclorg/nginx-container.git --context-dir=1.12/test/test-app/ rhscl/nginx-112-rhel7 nginx-sample-app
    $ docker run -p 8080:8080 nginx-sample-app
    ```
    
*  **For CentOS based image**
    ```
    $ s2i build https://github.com/sclorg/nginx-container.git --context-dir=1.12/test/test-app/ centos/nginx-112-centos7 nginx-sample-app
    $ docker run -p 8080:8080 nginx-sample-app
    ```

**Accessing the application:**
```
$ curl 127.0.0.1:8080
```


S2I build support
-------------
Nginx server image can be extended using S2I tool (see Usage section).
S2I build folder structure:

|    Folder name              |    Description                            |
| :-------------------------- | ----------------------------------------- |
|  ./nginx-cfg/*.conf         | Should contain all nginx configuration we want to include into image |
|  ./nginx-default-cfg/*.conf | Contains any nginx config snippets to include in the default server block |
|  ./nginx-pre-init/*.sh | Contains shell scripts that are sourced right before nginx is launched |
|  ./                         | Should contain nginx application source code                         |

Environment variables and volumes
-------------
The nginx container image supports the following configuration variable, which can be set by using the `-e` option with the docker run command:


|    Variable name       |    Description                            |
| :--------------------- | ----------------------------------------- |
|  `NGINX_LOG_TO_VOLUME` | When `NGINX_LOG_TO_VOLUME` is set, nginx logs into `/var/opt/rh/rh-nginx112/log/nginx/` |

You can mount your own web root like this:
```
$ docker run -v <DIR>:/var/www/html/ <container>
```
You can replace \<DIR> with location of your web root. Please note that this has to be an **absolute** path, due to Docker requirements.


Troubleshooting
---------------
By default, nginx logs into standard output, so the log is available in the container log. The log can be examined by running:

    docker logs <container>

**If `NGINX_LOG_TO_VOLUME` variable is set, nginx logs into `/var/opt/rh/rh-nginx112/log/nginx/`, which can be mounted to host system using the Docker volumes.**


See also
--------
Dockerfile and other sources for this container image are available on
https://github.com/sclorg/nginx-container.
In that repository, Dockerfile for CentOS is called Dockerfile, Dockerfile
for RHEL is called Dockerfile.rhel7.
