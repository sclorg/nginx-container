#!/bin/bash

set -eu

if [ ! -v NGINX_LOG_TO_VOLUME ]; then
    sed -ri ' s!^(\s*access_log)\s+\S+!\1 /proc/self/fd/1!g; s!^(\s*error_log)\s+\S+!\1 /proc/self/fd/2;!g;' /opt/rh/nginx16/root/etc/nginx/nginx.conf
fi

exec "$@"
