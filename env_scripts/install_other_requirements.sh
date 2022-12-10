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

benchmark_info "Install other packages"

function pip_install() {
    PACKAGENAME="$1"
    $PYTHON -c "from importlib.metadata import version; version('${PACKAGENAME}')" 2> /dev/null
    if [ $? -ne 0 ]; then

        benchmark_info "Installing ${PACKAGENAME}"

        $PYTHON -m pip install ${PACKAGENAME} -i ${HUAWEI_PIP}
    else
        pkg_installed_info ${PACKAGENAME}
    fi
}

pip_install "openfermionpyscf"
pip_install "toml"
