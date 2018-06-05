FROM centos/s2i-core-centos7

# RHSCL rh-nginx18 image.
#
# Volumes:
#  * /var/opt/rh/rh-nginx18/log/nginx/ - Storage for logs

EXPOSE 8080
EXPOSE 8443

ENV NAME=nginx \
    NGINX_VERSION=1.8 \
    NGINX_SHORT_VER=18 \
    VERSION=0

ENV SUMMARY="Platform for running nginx $NGINX_VERSION or building nginx-based application" \
    DESCRIPTION="Nginx is a web server and a reverse proxy server for HTTP, SMTP, POP3 and IMAP \
protocols, with a strong focus on high concurrency, performance and low memory usage. The container \
image provides a containerized packaging of the nginx $NGINX_VERSION daemon. The image can be used \
as a base image for other applications based on nginx $NGINX_VERSION web server. \
Nginx server image can be extended using source-to-image tool."

LABEL summary="${SUMMARY}" \
      description="${DESCRIPTION}" \
      io.k8s.description="${DESCRIPTION}" \
      io.k8s.display-name="Nginx ${NGINX_VERSION}" \
      io.openshift.expose-services="8080:http" \
      io.openshift.expose-services="8443:https" \
      io.openshift.tags="builder,${NAME},rh-${NAME}${NGINX_SHORT_VER}" \
      com.redhat.component="rh-${NAME}${NGINX_SHORT_VER}-docker" \
      name="centos/${NAME}-${NGINX_SHORT_VER}-centos7" \
      version="${NGINX_VERSION}" \
      maintainer="SoftwareCollections.org <sclorg@redhat.com>" \
      help="For more information visit https://github.com/sclorg/${NAME}-container" \
      usage="s2i build <SOURCE-REPOSITORY> centos/${NAME}-${NGINX_SHORT_VER}-centos7:latest <APP-NAME>"

ENV NGINX_CONFIGURATION_PATH=${APP_ROOT}/etc/nginx.d \
    NGINX_DEFAULT_CONF_PATH=${APP_ROOT}/etc/nginx.default.d \
    NGINX_CONTAINER_SCRIPTS_PATH=/usr/share/container-scripts/nginx \
    NGINX_APP_ROOT=${APP_ROOT}

RUN yum install -y yum-utils gettext hostname && \
    yum install -y centos-release-scl-rh && \
    INSTALL_PKGS="nss_wrapper bind-utils rh-nginx18 rh-nginx18-nginx" && \
    yum install -y --setopt=tsflags=nodocs $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    yum clean all

# Copy the S2I scripts from the specific language image to $STI_SCRIPTS_PATH
COPY ./s2i/bin/ $STI_SCRIPTS_PATH

# Copy extra files to the image.
COPY ./root/ /

# In order to drop the root user, we have to make some directories world
# writeable as OpenShift default security model is to run the container under
# random UID.
RUN sed -i -f ${NGINX_APP_ROOT}/nginxconf.sed /etc/opt/rh/rh-nginx18/nginx/nginx.conf && \
    mkdir -p ${NGINX_APP_ROOT}/etc/nginx.d/ && \
    mkdir -p ${NGINX_APP_ROOT}/etc/nginx.default.d/ && \
    mkdir -p ${NGINX_APP_ROOT}/src/nginx-start/ && \
    mkdir -p ${NGINX_CONTAINER_SCRIPTS_PATH}/nginx-start && \
    chmod -R a+rwx ${NGINX_APP_ROOT}/etc && \
    chmod -R a+rwx /var/opt/rh/rh-nginx18 && \
    chmod -R a+rwx ${NGINX_CONTAINER_SCRIPTS_PATH}/nginx-start && \
    chown -R 1001:0 ${NGINX_APP_ROOT} && \
    chown -R 1001:0 /var/opt/rh/rh-nginx18 && \
    chown -R 1001:0 ${NGINX_CONTAINER_SCRIPTS_PATH}/nginx-start && \
    rpm-file-permissions

USER 1001

# Not using VOLUME statement since it's not working in OpenShift Online:
# https://github.com/sclorg/httpd-container/issues/30
# VOLUME ["/opt/rh/rh-nginx18/root/usr/share/nginx/html"]
# VOLUME ["/var/opt/rh/rh-nginx18/log/nginx/"]

ENV BASH_ENV=${NGINX_APP_ROOT}/etc/scl_enable \
    ENV=${NGINX_APP_ROOT}/etc/scl_enable \
    PROMPT_COMMAND=". ${NGINX_APP_ROOT}/etc/scl_enable"

CMD $STI_SCRIPTS_PATH/usage
