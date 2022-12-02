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
"""Benchmark random hamiltonian expectation on qiskit."""
from benchmark.task_preparation import generate_random_ham
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer import AerSimulator


def trans_ham(n_qubits: int):
    ham_text = generate_random_ham(n_qubits)
    out = []
    for i in ham_text:
        tmp = ['I'] * n_qubits
        for p, idx in i:
            tmp[idx] = p
        out.append(''.join(tmp[::-1]))
    return SparsePauliOp(out)


def qiskit_random_ham_prepare(platform: str, n_qubits: int):
    if platform == 'cpu':
        Simulator = AerSimulator(method='statevector', device='CPU')
    elif platform == 'gpu':
        Simulator = AerSimulator(method='statevector', device='GPU')
    else:
        raise RuntimeError("qiskit do not support platform " + platform)
    circ = QuantumCircuit(n_qubits)
    for i in range(n_qubits):
        circ.h(i)

    ham = trans_ham(n_qubits)
    circ.save_expectation_value(ham, list(range(n_qubits)))

    def run():
        return Simulator.run(circ).result().data()['expectation_value']

    return run


if __name__ == '__main__':
    run = quest_random_ham_prepare('gpu', 5)
    print(run())
