/listen/s%80%8080%
s/^user *nginx;//
s%/etc/opt/rh/rh-nginx18/nginx/conf.d/%/opt/app-root/etc/nginx.d/%
s%/opt/rh/rh-nginx18/root/usr/share/nginx/html%/opt/app-root/src%
/#charset koi8-r;/a \\tinclude /opt/app-root/etc/nginx.default.d/*.conf;
