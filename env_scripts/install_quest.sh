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

if [ ! -f $python_venv_path/lib/libQuEST.so ]; then

    echo "Installing quest"
    URL=https://gitee.com/donghufeng/QuEST.git
    PACKAGENAME="QuEST"
    PACKAGEPATH=${third_party}/${PACKAGENAME}

    if [ ! -d $third_party ]; then
        mkdir $third_party
    fi

    cd $third_party
    if [ ! -d ${PACKAGEPATH} ]; then
        git clone $URL
    fi
    cd $PACKAGEPATH

    if [ -d build ]; then
        rm -rf build
    fi
    mkdir build
    cd build
    cmake .. -DGPUACCELERATED=1 -DGPU_COMPUTE_CAPABILITY=60
    make -j10
    cp QuEST/libQuEST.so $python_venv_path/lib
    # cd ..
    # rm -rf build
    # mkdir build
    # cd build
    # cmake ..
    # make -j10
    # cp QuEST/libQuEST.so $python_venv_path/lib/libQuEST.so
    export LD_LIBRARY_PATH=${python_venv_path}/lib:${LD_LIBRARY_PATH}

    cd $ROOTDIR
else
    echo "${_BOLD}${_RED}quest already installed.${_NORMAL}"
fi
