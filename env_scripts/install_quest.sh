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

$PYTHON -c "import quest_test" 2> /dev/null

if [ $? -ne 0 ]; then

    benchmark_info "Installing quest"
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

    PYBIND_DIR=$($PYTHON -c "import pybind11;print(pybind11.get_cmake_dir())")
    if [ $? -ne 0 ]; then
        benchmark_info "Cannot import pybind11, install it."
        $PYTHON -m pip install pybind11==2.10.0
        PYBIND_DIR=$($PYTHON -c "import pybind11;print(pybind11.get_cmake_dir())")
    else
        pkg_installed_info "pybind11"
    fi

    mkdir build
    cd build
    cmake -Dpybind11_DIR=${PYBIND_DIR} ..
    make -j10
    cp QuEST/libQuEST.so $python_venv_path/lib
    export LD_LIBRARY_PATH=${python_venv_path}/lib:${LD_LIBRARY_PATH}
    cd $ROOTDIR

    if [ "$_IS_GITHUB_CI" -ne 1 ]; then
        cd $third_party
        cd $PACKAGEPATH
        if [ -d build ]; then
            rm -rf build
        fi
        mkdir build
        cd build
        cmake .. -DGPUACCELERATED=1 -DGPU_COMPUTE_CAPABILITY=60 -Dpybind11_DIR=${PYBIND_DIR}
        make -j10
        cp QuEST/libQuEST.so $python_venv_path/lib/libQuEST_GPU.so

        cd $ROOTDIR
    fi

    $PYTHON -c "import quest_test" 2> /dev/null

    if [ $? -ne 0 ]; then
        pkg_installed_info "quest"
        if [ -d build ]; then
            rm -rf build
        fi
        mkdir build
        cd build
        if [ "$_IS_GITHUB_CI" -eq 1 ]; then
            cmake -Dpybind11_DIR=${PYBIND_DIR} -DUNABLE_GPU=ON -DOUTPUT_DIR=${SITE_PACKAGES} ..
        else
            cmake -Dpybind11_DIR=${PYBIND_DIR} -DOUTPUT_DIR=${SITE_PACKAGES} ..
        fi
        make -j8
        cd $ROOTDIR
        ls ${SITE_PACKAGES}/*.so
    fi

    $PYTHON -c "import quest_test" 2> /dev/null
    if [ $? -ne 0 ]; then
            die "Install quest failed."
    else
        pkg_installed_info "quest"
    fi
else
    pkg_installed_info "quest"
fi
