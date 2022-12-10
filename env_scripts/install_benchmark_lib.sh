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

$PYTHON -m pip install --upgrade pip -i ${TUNA_PIP}

if [ "${BENCHMARK_MINDQUANTUM}:-1" == "1" ]; then
    . "$BASEPATH/install_mindquantum.sh"
fi

if [ "${BENCHMARK_INTEL}:-1" == "1"]; then
    . "$BASEPATH/install_intel_qs.sh"
fi

if [ "${BENCHMARK_PADDLEQUANTUM}:-1" == "1" ]; then
    . "$BASEPATH/install_paddlequantum.sh"
fi

if [ "${BENCHMARK_QISKIT}:-1" == "1" ]; then
    . "$BASEPATH/install_qiskit.sh"
fi

if [ "${BENCHMARK_TFQ}:-1" == "1" ]; then
    . "$BASEPATH/install_tfq.sh"
fi

if [ "${BENCHMARK_QULACS}:-1" == "1" ]; then
    . "$BASEPATH/install_qulacs.sh"
fi

if [ "${BENCHMARK_QUEST}:-1" == "1" ]; then
    . "$BASEPATH/install_quest.sh"
fi

if [ "${BENCHMARK_TENSORCIRCUIT}:-1" == "1" ]; then
    . "$BASEPATH/install_tensorcircuit.sh"
fi

if [ "${BENCHMARK_PYQPANDA}:-1" == "1" ]; then
    . "$BASEPATH/install_pyqpanda.sh"
fi

. "$BASEPATH/install_other_requirements.sh"
