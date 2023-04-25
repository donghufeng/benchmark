# Copyright 2021 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http: //www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
from qulacs import (
    GradCalculator,
    Observable,
    ParametricQuantumCircuit,
    QuantumCircuit,
    QuantumState,
    gate,
)

from mindquantum import qft
from benchmark.translator.qulacs import mq_circ_to_qulacs

def qulacs_qft_prepare(backend:str, n_qubits: str):
    if backend == "gpu":
        from qulacs_core import QuantumStateGpu
        QuantumState = QuantumStateGpu
    elif backend == "cpu":
        from qulacs import QuantumState
    else:
        raise RuntimeError(f"platform {backend} not supported by qulacs.")

    circ = mq_circ_to_qulacs(qft(range(n_qubits)))
    state = QuantumState(n_qubits)
    def run():
        circ.update_quantum_state(state)
        return state

    return run
