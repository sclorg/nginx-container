/listen/s%80%8080 default_server%
s/^user *nginx;//

# See: https://github.com/sclorg/nginx-container/pull/69
/error_page/d
/40x.html/,+1d
/50x.html/,+1d
