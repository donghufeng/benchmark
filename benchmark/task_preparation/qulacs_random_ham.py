# Copyright 2021 Huawei Technologies Co., Ltd
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
# ============================================================================
"""Generate random hamiltonian of qulacs."""
from qulacs import Observable, QuantumCircuit


def qulacs_random_ham(n_qubit) -> Observable:
    qo = Observable(n_qubit)
    for i in range(n_qubit - 3):
        qo.add_operator(1, f"Y {i} Y {i+1} Y {i+2} Y {i+3}")
        qo.add_operator(1, f"X {i} X {i+2}")
        qo.add_operator(1, f"Z {i+1} Z {i+3}")
        qo.add_operator(1, f"Z {i} Y {i+1} X {i+2} Z {i+3}")
    return qo


def qulacs_random_ham_prepare(platform: str, n_qubits: int):
    if platform == "gpu":
        from qulacs_core import QuantumStateGpu as QuantumState
    elif platform == "cpu":
        from qulacs import QuantumState
    else:
        raise RuntimeError(f"platform {platform} not supported by qulacs.")
    qo = qulacs_random_ham(n_qubits)
    qulacs_states = QuantumState(n_qubits)
    init_circ = QuantumCircuit(n_qubits)
    for i in range(n_qubits):
        init_circ.add_H_gate(i)
    init_circ.update_quantum_state(qulacs_states)

    def run():
        return qo.get_expectation_value(qulacs_states)

    return run


if __name__ == "__main__":
    from qulacs import QuantumCircuit, QuantumState
    from qulacs_core import QuantumStateGpu

    n_qubit = 15
    qulacs_states = QuantumState(n_qubit)
    qo = qulacs_random_ham(n_qubit)
    res = qo.get_expectation_value(qulacs_states)
