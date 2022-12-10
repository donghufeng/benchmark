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

# ------------------------------------------------------------------------------
. "$BASEPATH/pip_url.sh"

if [ -z "$SED" ]; then
    if command -v gsed >/dev/null 2>&1; then
        SED='gsed'
    elif command -v awk >/dev/null 2>&1; then
        SED='sed'
    else
        echo 'ERROR: Unable to locate gsed or sed!' 1>&2
    fi
fi

function has_framework() {
    local fw="$1"
    local filename="$2"
    frameworks=$($SED -e 's/frameworks *= */frameworks = /' "$filename" \
                | $SED -n '/frameworks =/,/^]$/p' \
                | $SED -e '/frameworks =/d' -e '/^]$/d' -e "s/'//g" -e 's/^ *//g' -e 's/,$//' \
                | sed -e '/# /d' \
                | tr '\n' ' ')
    if [ -z "$frameworks" ]; then
        die "Failed to parse [benchmark-framework.frameworks] from $filename"
    fi
    find_it=0
    for pkg in $frameworks; do
        if [[ $pkg == $fw ]]; then
            find_it=1
            benchmark_info "task requires framework: ${fw}"
            break
        fi
    done
}
