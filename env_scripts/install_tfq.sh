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

$PYTHON -c "from importlib.metadata import version; version('tensorflow_quantum')"
if [ $? -ne 0 ]; then

    echo "Installing tensorflow_quantum"

    $PYTHON -m pip install tensorflow==2.7.0 -i ${HUAWEI_PIP}
    $PYTHON -m pip install tensorflow_quantum==0.7.2 -i ${HUAWEI_PIP}
else
    echo "${_BOLD}${_RED}tensorflow quantum already installed.${_NORMAL}"
fi
