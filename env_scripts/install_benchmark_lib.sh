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

# ------------------------------------------------------------------------------

. "$BASEPATH/pip_url.sh"
. "$BASEPATH/parse_framework.sh"

$PYTHON -m pip install --upgrade pip -i ${TUNA_PIP}

has_framework "mindquantum" $1
if [ $find_it -eq 1 ]; then
    benchmark_info "Install MINDQUANTUM"
    . "$BASEPATH/install_mindquantum.sh"
fi

has_framework "intel" $1
if [ $find_it -eq 1 ]; then
    benchmark_info "Install INTEL"
    . "$BASEPATH/install_intel_qs.sh"
fi

has_framework "paddlequantum" $1
if [ $find_it -eq 1 ]; then
    benchmark_info "Install PADDLEQUANTUM"
    . "$BASEPATH/install_paddlequantum.sh"
fi

has_framework "qiskit" $1
if [ $find_it -eq 1 ]; then
    benchmark_info "Install QISKIT"
    . "$BASEPATH/install_qiskit.sh"
fi

has_framework "tensorflowquantum" $1
if [ $find_it -eq 1 ]; then
    benchmark_info "Install TensorFlow Quantum"
    . "$BASEPATH/install_tfq.sh"
fi

has_framework "qulacs" $1
if [ $find_it -eq 1 ]; then
    benchmark_info "Install QULACS"
    . "$BASEPATH/install_qulacs.sh"
fi

has_framework "quest" $1
if [ $find_it -eq 1 ]; then
    benchmark_info "Install QUEST"
    . "$BASEPATH/install_quest.sh"
fi

has_framework "tensorcircuit" $1
if [ $find_it -eq 1 ]; then
    benchmark_info "Install TENSORCIRCUIT"
    . "$BASEPATH/install_tensorcircuit.sh"
fi

has_framework "pyqpanda" $1
if [ $find_it -eq 1 ]; then
    benchmark_info "Install PYQPANDA"
    . "$BASEPATH/install_pyqpanda.sh"
fi

. "$BASEPATH/install_other_requirements.sh"
