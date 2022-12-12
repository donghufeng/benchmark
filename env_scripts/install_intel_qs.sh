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

$PYTHON -c "import intelqs_py" 2> /dev/null

if [ $? -ne 0 ]; then
    benchmark_info "Install intel-qs"

    URL="https://gitee.com/mirrors_intel/Intel-QS.git"
    if [ ! -d $third_party ]; then
        mkdir $third_party
    fi

    cd $third_party

    if [ ! -d $PACKAGEPATH ]; then
        git clone $URL
    fi

    cd $PACKAGEPATH
    benchmark_info "Building ${PACKAGENAME}"

    if [ ! -d "build" ]; then
        mkdir build
    else
        rm -r build
        mkdir build
    fi

    PYBIND_DIR=$($PYTHON -c "import pybind11;print(pybind11.get_cmake_dir())")
    if [ $? -ne 0 ]; then
        benchmark_info "Cannot import pybind11, install it."
        $PYTHON -m pip install pybind11==2.10.0
        PYBIND_DIR=$($PYTHON -c "import pybind11;print(pybind11.get_cmake_dir())")
    else
        pkg_installed_info "pybind11"
    fi

    benchmark_info "pybind_DIR is ${PYBIND_DIR}"

    cd build
    cmake -DIqsMPI=OFF -DIqsUtest=OFF -DIqsPython=ON -DIqsNoise=OFF -DBuildExamples=OFF -Dpybind11_DIR=$PYBIND_DIR ..
    make -j10
    cp lib/*.so ${SITE_PACKAGES}
    cd $ROOTDIR
    $PYTHON -c "import intelqs_py;print(intelqs_py.__file__)"
    if [ $? -ne 0 ]; then
        die "Install intel_qs failed."
    else
        pkg_installed_info "intel-qs"
    fi
else
    pkg_installed_info "intel-qs"
fi
