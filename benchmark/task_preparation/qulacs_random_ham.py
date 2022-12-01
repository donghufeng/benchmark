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

from benchmark.task_preparation import generate_random_ham


def qulacs_random_ham(n_qubit) -> Observable:
    ham_text = generate_random_ham(n_qubit)
    qo = Observable(n_qubit)
    for term in ham_text:
        qo.add_operator(1, " ".join(f"{i} {j}" for i, j in term))
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
    run = qulacs_random_ham_prepare("cpu", 4)
    print(run())
