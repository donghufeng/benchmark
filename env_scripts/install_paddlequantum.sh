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

$PYTHON -c "from importlib.metadata import version; version('paddle_quantum')"

if [ $? -ne 0 ]; then

    echo "Install paddlepaddle quantum"
    $PYTHON -m pip install paddle-quantum

    echo "Install paddle"
    $PYTHON -m pip install paddlepaddle-gpu==2.4.0rc0

    $PYTHON -m pip install openfermion --upgrade

else

    echo "${_BOLD}${_RED}paddle quantum already installed.${_NORMAL}"

fi
