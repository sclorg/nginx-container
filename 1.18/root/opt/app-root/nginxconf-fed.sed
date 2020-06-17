/listen/s%80%8080%
s/^user *nginx;//
s%/etc/nginx/conf.d/%/opt/app-root/etc/nginx.d/%
s%/etc/nginx/default.d/%/opt/app-root/etc/nginx.default.d/%
s%/usr/share/nginx/html%/opt/app-root/src%
