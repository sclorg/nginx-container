Nginx container images
===================

This repository contains Dockerfiles for Nginx images for OpenShift.
Users can choose between RHEL and CentOS based images.

For more information about contributing, see
[the Contribution Guidelines](https://github.com/sclorg/welcome/blob/master/contribution.md).
For more information about concepts used in these container images, see the
[Landing page](https://github.com/sclorg/welcome).


Versions
---------------
Nginx versions currently provided are:
* [nginx-1.10](1.10)
* [nginx-1.14](1.14)

RHEL versions currently supported are:
* RHEL7
* RHEL8

CentOS versions currently supported are:
* CentOS7


Installation
----------------------
Choose either the CentOS7 or RHEL7 based image:

*  **RHEL7 based image**

    These images are available in the [Red Hat Container Catalog](https://access.redhat.com/containers/#/registry.access.redhat.com/rhscl/nginx-114-rhel7).
    To download it run:

    ```
    $ podman pull registry.access.redhat.com/rhscl/nginx-114-rhel7
    ```

    To build a RHEL7 based Nginx image, you need to run Docker build on a properly
    subscribed RHEL machine.

    ```
    $ git clone --recursive https://github.com/sclorg/nginx-container.git
    $ cd nginx-container
    $ git submodule update --init
    $ make build TARGET=rhel7 VERSIONS=1.14
    ```

*  **CentOS7 based image**

    This image is available on DockerHub. To download it run:

    ```
    $ podman pull centos/nginx-114-centos7
    ```

    To build a CentOS based Nginx image from scratch, run:

    ```
    $ git clone --recursive https://github.com/sclorg/nginx-container.git
    $ cd nginx-container
    $ git submodule update --init
    $ make build TARGET=centos7 VERSIONS=1.14
    ```

For using other versions of Nginx, just replace the `1.14` value by particular version
in the commands above.

Note: while the installation steps are calling `podman`, you can replace any such calls by `docker` with the same arguments.

**Notice: By omitting the `VERSIONS` parameter, the build/test action will be performed
on all provided versions of Nginx, which must be specified in  `VERSIONS` variable.
This variable must be set to a list with possible versions (subdirectories).**


Usage
---------------------------------

For information about usage of Dockerfile for nginx 1.10,
see [usage documentation](1.10).

For information about usage of Dockerfile for nginx 1.14,
see [usage documentation](1.14).


Build
---------------------------------
Images can be built using `make` command.

```
$ cd nginx-container
$ git submodule update --init
$ make build TARGET=centos7 VERSIONS=1.14
```

For more information about make rules see [README](https://github.com/sclorg/container-common-scripts/blob/master/README.md).

Test
---------------------------------

This repository also provides a test framework, which checks basic functionality
of the Nginx image.

Users can choose between testing Nginx based on a RHEL or CentOS image.

*  **RHEL based image**

    To test a RHEL7 based Nginx image, you need to run the test on a properly
    subscribed RHEL machine.

    ```
    $ cd nginx-container
    $ git submodule update --init
    $ make test TARGET=rhel7 VERSIONS=1.14
    ```

*  **CentOS based image**

    ```
    $ cd nginx-container
    $ git submodule update --init
    $ make test TARGET=centos7 VERSIONS=1.14
    ```

For using other versions of Nginx, just replace the `1.14` value by particular version
in the commands above.

**Notice: By omitting the `VERSIONS` parameter, the build/test action will be performed
on all provided versions of Nginx, which must be specified in  `VERSIONS` variable.
This variable must be set to a list with possible versions (subdirectories).**
