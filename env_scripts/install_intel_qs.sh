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

PACKAGENAME="Intel-QS"
PACKAGEPATH="${third_party}/${PACKAGENAME}"

export PYTHONPATH=${PACKAGEPATH}/build/lib:$PYTHONPATH

$PYTHON -c "import intelqs_py"

if [ $? -ne 0 ]; then

    URL="https://gitee.com/mirrors_intel/Intel-QS.git"
    if [ ! -d $third_party ]; then
        mkdir $third_party
    fi

    cd $third_party

    if [ ! -d $PACKAGEPATH ]; then
        git clone $URL
    fi

    cd $PACKAGEPATH
    echo "Building ${PACKAGENAME}"

    if [ ! -d "build" ]; then
        mkdir build
    else
        rm -r build
        mkdir build
    fi

    $PYTHON -c "import pybind11"
    if [ $? -ne 0 ]; then
        $PYTHON -m pip install pybind11==2.10.0
    fi
    PYBIND_DIR=$($PYTHON -m pybind11 --cmakedir)
    cd build
    cmake -DIqsMPI=OFF -DIqsUtest=OFF -DIqsPython=ON -DIqsNoise=OFF -DBuildExamples=OFF -Dpybind11_DIR=$PYBIND_DIR ..
    make -j10
    cp lib/*.so ${python_venv_path}/bin
    cd $ROOTDIR

else
    echo "${_BOLD}${_RED}intel-qs already installed.${_NORMAL}"
fi
