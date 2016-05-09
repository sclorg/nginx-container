s/^        listen       80/        listen       8080/
s/^user  nginx;//
s%/etc/opt/rh/rh-nginx18/nginx/conf.d/%/opt/app-root/etc/nginx.d/%
s%/opt/rh/rh-nginx18/root/usr/share/nginx/html%/opt/app-root/src%
s%/var/opt/rh/rh-nginx18/log/nginx/error.log%stderr%
s%access_log  /var/opt/rh/rh-nginx18/log/nginx/access.log  main;%%
