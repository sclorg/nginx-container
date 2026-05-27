Nginx container images
======================

[![Build and push container images to quay.io registry](https://github.com/sclorg/nginx-container/actions/workflows/build-and-push.yml/badge.svg)](https://github.com/sclorg/nginx-container/actions/workflows/build-and-push.yml)

This repository contains Dockerfiles for Nginx images for OpenShift.
Users can choose between RHEL, Fedora, CentOS and CentOS Stream based images.

For more information about contributing, see
[the Contribution Guidelines](https://github.com/sclorg/welcome/blob/master/contribution.md).
For more information about concepts used in these container images, see the
[Landing page](https://github.com/sclorg/welcome).


Versions
--------
Currently supported versions are visible in the following table, expand an entry to see its container registry address.
<!--
Table start
-->
||CentOS Stream 9|CentOS Stream 10|Fedora|RHEL 8|RHEL 9|RHEL 10|
|:--|:--:|:--:|:--:|:--:|:--:|:--:|
|1.20||||<details><summary>✓</summary>`registry.redhat.io/rhel8/nginx-120`</details>|||
|1.22||||<details><summary>✓</summary>`registry.redhat.io/rhel8/nginx-122`</details>|<details><summary>✓</summary>`registry.redhat.io/rhel9/nginx-122`</details>||
|1.22-micro|<details><summary>✓</summary>`quay.io/sclorg/nginx-122-micro-c9s`</details>|||<details><summary>✓</summary>`registry.redhat.io/rhel8/nginx-122-micro`</details>|||
|1.24|<details><summary>✓</summary>`quay.io/sclorg/nginx-124-c9s`</details>|||<details><summary>✓</summary>`registry.redhat.io/rhel8/nginx-124`</details>|<details><summary>✓</summary>`registry.redhat.io/rhel9/nginx-124`</details>||
|1.26|<details><summary>✓</summary>`quay.io/sclorg/nginx-126-c9s`</details>|<details><summary>✓</summary>`quay.io/sclorg/nginx-126-c10s`</details>|<details><summary>✓</summary>`quay.io/fedora/nginx-126`</details>||<details><summary>✓</summary>`registry.redhat.io/rhel9/nginx-126`</details>|<details><summary>✓</summary>`registry.redhat.io/rhel10/nginx-126`</details>|
<!--
Table end
-->


Installation
----------------------
Choose either the CentOS Stream 9 or RHEL8 based image:

*  **RHEL8 based image**

    These images are available in the [Red Hat Container Catalog](https://access.redhat.com/containers/#/registry.access.redhat.com/rhel8/nginx-124).
    To download it run:

    ```
    $ podman pull registry.access.redhat.com/rhel9/nginx-124
    ```

    To build a RHEL8 based Nginx image, you need to run Docker build on a properly
    subscribed RHEL machine.

    ```
    $ git clone --recursive https://github.com/sclorg/nginx-container.git
    $ cd nginx-container
    $ git submodule update --init
    $ make build TARGET=rhel9 VERSIONS=1.24
    ```

*  **CentOS Stream based image**

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


## Contributing Guidelines

This repository utilizes [distgen](https://github.com/devexp-db/distgen/) for generating image source files. If you are interested in updating a Dockerfile, please modify the relevant sections in the `specs/multispec.yml` file and/or the `Dockerfile.template` (or other distgen files), and then execute `make generate`.

Before you begin, ensure that you have `distgen` installed by running `dg --version`. If `distgen` is not installed on your system, follow the installation guide available at [distgen's GitHub repository](https://github.com/devexp-db/distgen/).
Additionally, for testing purposes, install `go-md2man` from this repository [go-md2man](https://github.com/cpuguy83/go-md2man) or via `dnf install go-md2man`.

To contribute, please follow these steps:

1. Fork the repository
2. Run `git submodule update --init` to download the `common` submodule containing the `common/common.mk` makefile.
3. Implement a new feature or bug fix in the templates (found in the `src` directory) or update values in the `specs/multispec.yml` file.
   - Note: If no changes are made to these directories, file regeneration is not necessary.
4. Regenerate all files by executing `make generate`.
5. Consider running CI tests, as described in the Test section below.
6. Commit the files and generated files in two separated commits with a conventional commit message for each.
7. Open a pull request for review!

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
$ make build TARGET=rhel9 VERSIONS=1.24
```

For more information about make rules see [README](https://github.com/sclorg/container-common-scripts/blob/master/README.md).

Test
---------------------------------

This repository also provides a test framework, which checks basic functionality
of the Nginx image.

Users can choose between testing Nginx based on a RHEL or CentOS image.

*  **RHEL based image**

    To test a RHEL8 based Nginx image, you need to run the test on a properly
    subscribed RHEL machine.

    ```
    $ cd nginx-container
    $ git submodule update --init
    $ make test TARGET=rhel9 VERSIONS=1.24
    ```

*  **CentOS Stream based image**

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
