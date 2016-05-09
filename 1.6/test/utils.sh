#!/usr/bin/env bash

function print_result {
    local RESET='\e[0m'
    local RED='\e[0;31m'
    local GREEN='\e[0;32m'
    local YELLOW='\e[1;33m'
    local PASS="${RESET}${GREEN}[PASS]"
    local FAIL="${RESET}${RED}[FAIL]"
    local WORKING="${RESET}${YELLOW}[....]"
    local STATUS="$1"
    shift

    if [ "${STATUS}" = pass ]; then
        echo -en "${PASS}"
    elif [ "${STATUS}" = fail ]; then
        echo -en "${FAIL}"
    elif [ "${STATUS}" = working ]; then
        echo -en "${WORKING}"
    else
        return
    fi

    echo -en " ${@}${RESET}"
    echo
}

function get_status {
    if [ "$1" = "$2" ]; then
        echo pass
    else
        echo fail
    fi
}

overall_res=0

# $1 is the exit code
function update_overall_result {
    res="$1"
    if [ "$res" != 0 ]; then
        overall_res="$res"
    fi
}

function get_overall {
    echo $overall_res
}

# Run command and print result (pass/fail) in pretty colors
# $1 should equal '1' if heads up should be printed
# $2 is the command
# $3 is the expected exit code (optional, defaults to 0)
# $4 is the message to be printed (optional)
function _run_command {
    local headsup="$1"
    local cmd="$2"
    local expected="${3:-0}"
    local msg="${4:-Running command '$cmd'}"
    if [ "$headsup" = 1 ]; then
        print_result working "$msg"
    fi
    eval $cmd
    local res="$?"
    status=`get_status "$res" "$expected"`
    print_result "$status" "$msg"
    update_overall_result "$res"
    return "$res"
}

# Run command and print result (pass/fail) in pretty colors
# $1 is the command
# $2 is the expected exit code (optional, defaults to 0)
# $3 is the message to be printed (optional)
function run_command {
    _run_command 0 "$@"
}

# Same as run_command, except that it also prints information about
# the command it is about to run
function run_command_headsup {
    _run_command 1 "$@"
}

function exit_overall {
    exit "$overall_res"
}
