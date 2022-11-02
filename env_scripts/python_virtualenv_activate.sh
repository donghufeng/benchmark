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

# shellcheck disable=SC2154

[ "${_sourced_python_virtualenv_activate}" != "" ] && return || _sourced_python_virtualenv_activate=.

BASEPATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && pwd )

# ------------------------------------------------------------------------------

# shellcheck source=SCRIPTDIR/common_functions.sh
. "$BASEPATH/common_functions.sh"

# ==============================================================================

if [ -z "$ROOTDIR" ]; then
    die '(internal error): ROOTDIR variable not defined!'
fi
if [ -z "$PYTHON" ]; then
    die '(internal error): PYTHON variable not defined!'
fi
if [ -z "$python_venv_path" ]; then
    die '(internal error): python_venv_path variable not defined!'
fi

# ==============================================================================

if [ -n "$VIRTUAL_ENV" ]; then
    debug_print "Currently activated virtualenv: $VIRTUAL_ENV"
    echo "Already inside a virtualenv, skipping activation"

    if [ "$do_update_venv" -eq 1 ]; then
        real_python_prefix=$("$PYTHON" -c 'import sys; print(sys.base_prefix)')
        for path_suffix in bin Scripts; do
            python_exec="$real_python_prefix/$path_suffix/$PYTHON"
            if [ -x "$python_exec" ]; then
                call_cmd "$python_exec" -m venv --upgrade "$python_venv_path"
            fi
        done
    fi
    return
fi

# ------------------------------------------------------------------------------

venv_args=( "$python_venv_path" )
if [[ "$VENV_USE_SYSTEM_PACKAGES" == "1" ]]; then
    venv_args+=( --system-site-packages )
fi

created_venv=0
if [ ! -d "$python_venv_path" ]; then
    # shellcheck disable=SC2034
    created_venv=1
    echo "Creating Python virtualenv: $PYTHON -m venv ${venv_args[*]}"
    call_cmd "$PYTHON" -m venv "${venv_args[@]}"
fi

echo "Activating Python virtual environment: $python_venv_path"
if [ -f "$python_venv_path/bin/activate" ]; then
    call_cmd source "$python_venv_path/bin/activate"
    debug_print "PATH=$PATH"
    hash -r
    debug_print "PYTHON = $(which "$PYTHON")"
elif [ -f "$python_venv_path/Scripts/activate" ]; then
    call_cmd source "$python_venv_path/Scripts/activate"
    # If on Windows, potentially need to fix the PATH format
    if command -v cygpath >/dev/null 2>&1; then
        new_path=$(cygpath --unix "$PATH")
        export PATH="$new_path"
    fi
    debug_print "PATH=$PATH"
    hash -r
    debug_print "PYTHON = $(which "$PYTHON")"
elif [ "${dry_run:-0}" -eq 1 ]; then
    call_cmd source "$python_venv_path/bin/activate"
else
    die 'Unable to activate Python virtual environment!'
fi

# ==============================================================================
