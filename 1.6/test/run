#!/usr/bin/env bash

IMAGE_NAME="${IMAGE_NAME:-rhscl/nginx-16-rhel7}"

. ./utils.sh

function create_container() {
    local name=$1 ; shift
    cidfile="$CIDFILE_DIR/$name"
    # create container with a cidfile in a directory for cleanup
    docker run ${DOCKER_ARGS:-} --cidfile $cidfile -d $IMAGE_NAME || return 1
    echo "Created container $(cat $cidfile)"
}

function get_cid() {
  local id="$1" ; shift || return 1
  echo $(cat "$CIDFILE_DIR/$id")
}

function check_default_page {
    curl localhost > output &&
    fgrep -e 'Test Page for the Nginx HTTP Server on Red Hat Enterprise Linux' output
}

function rm_container {
    local name="$1"
    local cid="`get_cid $name`"
    docker kill "$cid"
    docker rm "$cid"
    rm -f "$CIDFILE_DIR/$name"
}

tmpdir=`mktemp -d`
pushd $tmpdir > /dev/null || exit 1

CIDFILE_DIR=cid_files
mkdir "$CIDFILE_DIR"

run_command_headsup "docker pull $IMAGE_NAME"

# Check default page
DOCKER_ARGS='-p 80:80'
run_command_headsup "create_container test_default_page"
# Wakey wakey...
sleep 2
run_command_headsup "check_default_page" 0 "Check that the default page is served."
DOCKER_ARGS=
rm_container test_default_page

# Check the NGINX_LOG_TO_VOLUME env variable
log_dir='/var/log/nginx16-logs'
run_command_headsup "ls -d $log_dir || mkdir $log_dir" 0 "Create local log directory"
run_command_headsup "rm -Rf '$log_dir/*'" 0 "Make sure the log dir is empty"
run_command_headsup "chcon -Rvt svirt_sandbox_file_t $log_dir" 0 'Change SELinux context on the log dir'
DOCKER_ARGS="-p 80:80 -e NGINX_LOG_TO_VOLUME=1 -v $log_dir:/var/log/nginx16"
run_command_headsup "create_container test_log_vol"
sleep 2
run_command_headsup "curl localhost > /dev/null"
ls $log_dir > output
run_command_headsup "grep -e '^access\\.log$' output" 0 "Checking that file access.log exists"
run_command_headsup "grep -e '^error\\.log$' output" 0 "Checking that file error.log exists"
DOCKER_ARGS=
rm_container test_log_vol
rm -Rf "$log_dir/*" # log dir cleanup

# Test that docker volume for DocumentRoot works
doc_root='/var/www/html'
run_command_headsup "ls -d $doc_root || mkdir -p $doc_root" 0 'Create document root'
run_command_headsup "echo hello > $doc_root/index.html"
run_command_headsup "chcon -Rvt svirt_sandbox_file_t /var/www/html" 0 'Change SELinux context on the document root'
DOCKER_ARGS="-p 80:80 -v $doc_root:/opt/rh/nginx16/root/usr/share/nginx/html"
run_command_headsup "create_container test_doc_root"
sleep 2
run_command_headsup "curl localhost > output" 0 'Getting the index page'
run_command_headsup "grep -e '^hello$' output" 0 'The page should contain "hello"'
rm -f "$doc_root/index.html"
DOCKER_ARGS=
rm_container test_doc_root

popd > /dev/null
rm -Rf "$tmpdir"

exit_overall
