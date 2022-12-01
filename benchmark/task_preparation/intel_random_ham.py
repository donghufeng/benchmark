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
"""Benchmark expectation of random ham on intel simulator."""
import intelqs_py as simulator

from benchmark.task_preparation import generate_random_ham


def ham_trans(ham_text):
    ham = []
    for term in ham_text:
        idx = []
        pauli = []
        for p, i in term:
            idx.append(i)
            pauli.append(ord(p) - ord("X") + 1)
        ham.append([idx, pauli])
    return ham


def intel_random_ham_prepare(n_qubits: int):
    psi = simulator.QubitRegister(n_qubits, "base", 0, 0)
    for i in range(n_qubits):
        psi.ApplyHadamard(i)
    ham = ham_trans(generate_random_ham(n_qubits))

    def run():
        e0 = 0
        for qidx, paulis in ham:
            e0 += psi.ExpectationValue(qidx, paulis, 1.0)
        return e0

    return run


if __name__ == "__main__":
    n_qubits = 4
    run = intel_random_ham_prepare(n_qubits)
    run()
