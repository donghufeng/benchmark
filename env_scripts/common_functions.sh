#!/bin/bash
# Copyright 2022 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# shellcheck disable=SC2154,SC2034

BASEPATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && pwd )

[ "${_sourced_common_functions}" != "" ] && return || _sourced_common_functions=.

# ==============================================================================

ncolors=$(tput colors 2> /dev/null)
if [ -n "$ncolors" ] && [ "$ncolors" -ge 16 ]; then
    _BOLD="$(tput bold)"
    _UNDERLINE="$(tput smul)"
    _STANDOUT="$(tput smso)"
    _NORMAL="$(tput sgr0)"
    _BLACK="$(tput setaf 0)"
    _RED="$(tput setaf 1)"
    _GREEN="$(tput setaf 2)"
    _YELLOW="$(tput setaf 3)"
    _BLUE="$(tput setaf 4)"
    _MAGENTA="$(tput setaf 5)"
    _CYAN="$(tput setaf 6)"
    _WHITE="$(tput setaf 7)"
    _GREY="$(tput setaf 8)"
fi
unset ncolors

function debug_print() {
    if [ "${verbose:-0}" -eq 1 ]; then
        echo "${_YELLOW}DEBUG $*${_NORMAL}" >&2
    fi
}

function die() {
    # complain to STDERR and exit with error
    echo "${_BOLD}${_RED}$*${_NORMAL}" >&2; exit 2;
}

call_cmd() {
    if [ "${dry_run:-0}" -ne 1 ]; then
        debug_print "Calling command: $*"
        if ! "$@"; then
            die "Command failed: $*"
        fi
        return 0
    else
        echo "$@"
        return 0
    fi
}
