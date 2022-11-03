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

$PYTHON -c "import qulacs"
if [ $? -ne 0 ]; then

    echo "Installing qulacs"
    dpkg -s libboost-dev > /dev/null
    if [ $? -ne 0 ]; then
        echo "Install boost"
        sudo apt-get install libboost-all-dev
    fi
    URL="https://gitee.com/donghufeng/qulacs"
    PACKAGENAME="qulacs"
    PACKAGEPATH="${third_party}/${PACKAGENAME}"

    if [ ! -d $third_party ]; then
        mkdir $third_party
    fi

    cd $third_party

    if [ ! -d $PACKAGEPATH ]; then
        git clone $URL
    fi
    cd $PACKAGEPATH
    USE_GPU=Yes $PYTHON setup.py install
    cd $ROOTDIR
else
    echo "${_BOLD}${_RED}qulacs already installed.${_NORMAL}"
fi