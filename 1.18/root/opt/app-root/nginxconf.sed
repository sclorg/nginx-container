/listen/s%80%8080%
s/^user *nginx;//
s%/etc/opt/rh/rh-nginx118/nginx/conf.d/%/opt/app-root/etc/nginx.d/%
s%/etc/opt/rh/rh-nginx118/nginx/default.d/%/opt/app-root/etc/nginx.default.d/%
s%/opt/rh/rh-nginx118/root/usr/share/nginx/html%/opt/app-root/src%
