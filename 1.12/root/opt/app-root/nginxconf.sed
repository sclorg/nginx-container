/listen/s%80%8080%
s/^user *nginx;//
s%/etc/opt/rh/rh-nginx112/nginx/conf.d/%/opt/app-root/etc/nginx.d/%
s%/etc/opt/rh/rh-nginx112/nginx/default.d/%/opt/app-root/etc/nginx.default.d/%
s%/opt/rh/rh-nginx112/root/usr/share/nginx/html%/opt/app-root/src%

# See: https://github.com/sclorg/nginx-container/pull/69
/error_page/d
/40x.html/,+1d
/50x.html/,+1d
