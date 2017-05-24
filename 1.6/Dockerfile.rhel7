FROM rhel7

# RHSCL nginx16 image.
#
# Volumes:
#  * /opt/rh/nginx16/root/usr/share/nginx/html - Datastore for nginx
#  * /var/log/nginx16 - Storage for logs when $NGINX_LOG_TO_VOLUME is set
# Environment:
#  * $NGINX_LOG_TO_VOLUME (optional) - When set, nginx will log into /var/log/nginx16

EXPOSE 80
EXPOSE 443

ENV NGINX_VERSION=1.10

ENV SUMMARY="Platform for running nginx $NGINX_VERSION or building nginx-based application" \
    DESCRIPTION="Nginx is a web server and a reverse proxy server for HTTP, SMTP, POP3 and IMAP \
protocols, with a strong focus on high concurrency, performance and low memory usage. The container \
image provides a containerized packaging of the nginx $NGINX_VERSION daemon. The image can be used \
as a base image for other applications based on nginx $NGINX_VERSION web server. \
Nginx server image can be extended using source-to-image tool."

LABEL summary="$SUMMARY" \
      description="$DESCRIPTION" \
      io.k8s.description="DESCRIPTION" \
      io.k8s.display-name="Nginx 1.6" \
      io.openshift.expose-services="80:http" \
      io.openshift.expose-services="443:https" \
      io.openshift.tags="builder,nginx,nginx16" \
      name="rhscl/nginx-16-rhel7" \
      version="1.6" \
      release="9.3" \
      com.redhat.component="nginx16-docker"

COPY run-*.sh /usr/local/bin/

# Copy extra files to the image.
COPY ./root/ /

RUN yum install -y yum-utils gettext hostname && \
    yum-config-manager --enable rhel-server-rhscl-7-rpms && \
    yum-config-manager --enable rhel-7-server-optional-rpms && \
    INSTALL_PKGS="bind-utils nginx16 nginx16-nginx" && \
    yum install -y --setopt=tsflags=nodocs $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    yum clean all

# When bash is started non-interactively, to run a shell script, for example it
# looks for this variable and source the content of this file. This will enable
# the SCL for all scripts without need to do 'scl enable'.
ENV BASH_ENV=/var/lib/nginx16/scl_enable \
    ENV=/var/lib/nginx16/scl_enable \
    PROMPT_COMMAND=". /var/lib/nginx16/scl_enable"


VOLUME ["/opt/rh/nginx16/root/usr/share/nginx/html"]
VOLUME ["/var/log/nginx16"]

ENTRYPOINT ["/usr/local/bin/run-nginx16.sh"]
CMD ["nginx", "-g", "daemon off;"]
