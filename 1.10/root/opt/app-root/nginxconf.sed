/listen/s%80%8080%
s/^user *nginx;//
s%/etc/opt/rh/rh-nginx110/nginx/conf.d/%/opt/app-root/etc/nginx.d/%
s%/etc/opt/rh/rh-nginx110/nginx/default.d/%/opt/app-root/etc/nginx.default.d/%
s%/opt/rh/rh-nginx110/root/usr/share/nginx/html%/opt/app-root/src%
s%/var/opt/rh/rh-nginx110/log/nginx/error.log%stderr%
s%access_log  /var/opt/rh/rh-nginx110/log/nginx/access.log  main;%%
