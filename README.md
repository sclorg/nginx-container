Nginx container images
======================

[![Build and push container images to quay.io registry](https://github.com/sclorg/nginx-container/actions/workflows/build-and-push.yml/badge.svg)](https://github.com/sclorg/nginx-container/actions/workflows/build-and-push.yml)

Images available on Quay are:
* CentOS Stream 9 [nginx-1.20](https://quay.io/repository/sclorg/nginx-120-c9s)
* Fedora [nginx-1.20](https://quay.io/repository/fedora/nginx-120)
* Fedora [nginx-1.22](https://quay.io/repository/fedora/nginx-122)
* Fedora [nginx-1.24](https://quay.io/repository/fedora/nginx-124)
* Fedora [nginx-1.26](https://quay.io/repository/fedora/nginx-126)
* Micro CentOS Stream 9 [nginx-1.22](https://quay.io/repository/sclorg/nginx-122-micro-c9s)
* Micro Fedora [nginx-1.22](https://quay.io/repository/fedora/nginx-122-micro)


This repository contains Dockerfiles for Nginx images for OpenShift.
Users can choose between RHEL, Fedora, CentOS and CentOS Stream based images.

For more information about contributing, see
[the Contribution Guidelines](https://github.com/sclorg/welcome/blob/master/contribution.md).
For more information about concepts used in these container images, see the
[Landing page](https://github.com/sclorg/welcome).


Versions
--------
Nginx versions currently provided are:
* [nginx-1.20](1.20)
* [nginx-1.22](1.22)
* [nginx-1.22 micro](1.22-micro)
* [nginx-1.24](1.24)
* [nginx-1.26](1.26)

RHEL versions currently supported are:
* RHEL8
* RHEL9

CentOS Stream versions currently supported are:
* CentOS Stream 9


Installation
----------------------
Choose either the CentOS Stream 9 or RHEL8 based image:

*  **RHEL8 based image**

    These images are available in the [Red Hat Container Catalog](https://access.redhat.com/containers/#/registry.access.redhat.com/rhel8/nginx-124).
    To download it run:

    ```
    $ podman pull registry.access.redhat.com/rhel8/nginx-124
    ```

    To build a RHEL8 based Nginx image, you need to run Docker build on a properly
    subscribed RHEL machine.

    ```
    $ git clone --recursive https://github.com/sclorg/nginx-container.git
    $ cd nginx-container
    $ git submodule update --init
    $ make build TARGET=rhel8 VERSIONS=1.24
    ```

<<<<<<< HEAD
*  **CentOS Stream based image**
||||||| parent of 8fc0bd0 (Update README's for using RHEL8 and CentOS Stream 9.)
*  **CentOS7 based image**
=======
*  **CentOS Stream 9 based image**
>>>>>>> 8fc0bd0 (Update README's for using RHEL8 and CentOS Stream 9.)

    This image is available on DockerHub. To download it run:

    ```
    $ podman pull quay.io/sclorg/nginx-124-c9s
    ```

    To build a CentOS based Nginx image from scratch, run:

    ```
    $ git clone --recursive https://github.com/sclorg/nginx-container.git
    $ cd nginx-container
    $ git submodule update --init
    $ make build TARGET=c9s VERSIONS=1.24
    ```

For using other versions of Nginx, just replace the `1.24` value by particular version
in the commands above.

Note: while the installation steps are calling `podman`, you can replace any such calls by `docker` with the same arguments.

**Notice: By omitting the `VERSIONS` parameter, the build/test action will be performed
on all provided versions of Nginx, which must be specified in  `VERSIONS` variable.
This variable must be set to a list with possible versions (subdirectories).**


Usage
-----

For information about usage of Dockerfile for nginx 1.20,
see [usage documentation](1.20).

For information about usage of Dockerfile for nginx 1.22,
see [usage documentation](1.22).

For information about usage of Dockerfile for nginx 1.24,
see [usage documentation](1.24).

For information about usage of Dockerfile for nginx 1.26,
see [usage documentation](1.26).

Build
-----
Images can be built using `make` command.

```
$ cd nginx-container
$ git submodule update --init
$ make build TARGET=rhel8 VERSIONS=1.22
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
    $ make test TARGET=rhel8 VERSIONS=1.24
    ```

*  **CentOS based image**

    ```
    $ cd nginx-container
    $ git submodule update --init
    $ make test TARGET=c9s VERSIONS=1.24
    ```

For using other versions of Nginx, just replace the `1.24` value by particular version
in the commands above.

**Notice: By omitting the `VERSIONS` parameter, the build/test action will be performed
on all provided versions of Nginx, which must be specified in  `VERSIONS` variable.
This variable must be set to a list with possible versions (subdirectories).**
