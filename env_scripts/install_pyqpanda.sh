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


if [ "$_IS_GITHUB_CI" -eq "1" ]; then
    $PYTHON -c "from importlib.metadata import version; version('pyqpanda')"

    if [ $? -ne 0 ]; then
        $PYTHON -m pip install pyqpanda
        $PYTHON -c "from importlib.metadata import version; version('pyqpanda')"
        if [ $? -ne 0 ]; then
            benchmark_info "Install pyqpanda failed"
        else
            pkg_installed_info "pyqpanda"
        fi
    else
        pkg_installed_info "pyqpanda"
    fi
else
    $PYTHON -c "from importlib.metadata import version; version('pyqpanda')"

    if [ $? -ne 0 ]; then

        echo "Install pyqpanda"
        URL=https://gitee.com/OriginQ/QPanda-2.git
        PACKAGENAME="QPanda-2"
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
        FIND_CUDA=ON
        if [ "$_IS_GITHUB_CI" -eq 1 ]; then
            FIND_CUDA=OFF
        fi
        PYBIND_DIR=$($PYTHON -c "import pybind11;print(pybind11.get_cmake_dir())")
        if [ $? -ne 0 ]; then
            benchmark_info "Cannot import pybind11, install it."
            $PYTHON -m pip install pybind11==2.10.0
            PYBIND_DIR=$($PYTHON -c "import pybind11;print(pybind11.get_cmake_dir())")
        else
            pkg_installed_info "pybind11"
        fi
        cmake -DFIND_CUDA=${FIND_CUDA} -DUSE_PYQPANDA=ON -DPYQPANDA_STUBGEN=OFF -DUSE_SIMD=ON -Dpybind11_DIR=${PYBIND_DIR} ..
        make -j8
        cd ../pyQPanda
        rm -rf ${SITE_PACKAGES}/pyqpanda*
        cp -r pyqpanda ${SITE_PACKAGES}
    else

        echo "${_BOLD}${_RED}pyqpanda already installed.${_NORMAL}"

    fi
fi
