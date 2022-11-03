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
"""Generate random circuit for qulacs."""
import numpy as np
from qulacs import (
    QuantumState,
    ParametricQuantumCircuit,
    QuantumCircuit,
    gate,
    Observable,
    GradCalculator,
)

from qulacs_core import QuantumStateGpu

from benchmark import SEED


def qulacs_random_circ(n_quits):
    np.random.seed(SEED)
    p0 = np.random.uniform(-1, 1, (n_quits - 3) * 11)
    circ = QuantumCircuit(n_quits)
    for i in range(n_quits - 3):
        circ.add_H_gate(i)
        circ.add_H_gate(i + 1)
        circ.add_H_gate(i + 2)
        circ.add_H_gate(i + 3)
        circ.add_RX_gate(i, p0[i * 11])
        circ.add_RX_gate(i + 1, p0[i * 11 + 1])
        circ.add_RX_gate(i + 2, p0[i * 11 + 2])
        circ.add_RX_gate(i + 3, p0[i * 11 + 3])
        circ.add_CNOT_gate(i, i + 1)
        circ.add_CNOT_gate(i + 1, i + 2)
        circ.add_CNOT_gate(i + 2, i + 3)
        circ.add_CNOT_gate(i + 3, i)
        circ.add_multi_Pauli_rotation_gate([i, i + 1], [1, 1], p0[i * 11 + 4])
        circ.add_multi_Pauli_rotation_gate([i + 1, i + 2], [2, 2],
                                           p0[i * 11 + 5])
        circ.add_multi_Pauli_rotation_gate([i + 2, i + 3], [3, 3],
                                           p0[i * 11 + 6])
        circ.add_S_gate(i)
        circ.add_S_gate(i + 1)
        circ.add_T_gate(i + 2)
        circ.add_T_gate(i + 3)
        circ.add_RY_gate(i + 1, p0[i * 11 + 7])
        circ.add_RY_gate(i + 2, p0[i * 11 + 8])
        circ.add_SWAP_gate(i, i + 3)
        circ.add_RX_gate(i + 0, p0[i * 11 + 9])
        circ.add_RX_gate(i + 3, p0[i * 11 + 10])
    return circ


def qulacs_random_pqc(n_quits):
    np.random.seed(SEED)
    p0 = np.random.uniform(-1, 1, (n_quits - 3) * 11)
    circ = ParametricQuantumCircuit(n_quits)
    for i in range(n_quits - 3):
        circ.add_H_gate(i)
        circ.add_H_gate(i + 1)
        circ.add_H_gate(i + 2)
        circ.add_H_gate(i + 3)
        circ.add_parametric_RX_gate(i, p0[i * 11])
        circ.add_parametric_RX_gate(i + 1, p0[i * 11 + 1])
        circ.add_parametric_RX_gate(i + 2, p0[i * 11 + 2])
        circ.add_parametric_RX_gate(i + 3, p0[i * 11 + 3])
        circ.add_CNOT_gate(i, i + 1)
        circ.add_CNOT_gate(i + 1, i + 2)
        circ.add_CNOT_gate(i + 2, i + 3)
        circ.add_CNOT_gate(i + 3, i)
        circ.add_parametric_multi_Pauli_rotation_gate([i, i + 1], [1, 1],
                                                      p0[i * 11 + 4])
        circ.add_parametric_multi_Pauli_rotation_gate([i + 1, i + 2], [2, 2],
                                                      p0[i * 11 + 5])
        circ.add_parametric_multi_Pauli_rotation_gate([i + 2, i + 3], [3, 3],
                                                      p0[i * 11 + 6])
        circ.add_S_gate(i)
        circ.add_S_gate(i + 1)
        circ.add_T_gate(i + 2)
        circ.add_T_gate(i + 3)
        circ.add_parametric_RY_gate(i + 1, p0[i * 11 + 7])
        circ.add_parametric_RY_gate(i + 2, p0[i * 11 + 8])
        circ.add_SWAP_gate(i, i + 3)
        circ.add_parametric_RX_gate(i + 0, p0[i * 11 + 9])
        circ.add_parametric_RX_gate(i + 3, p0[i * 11 + 10])
    return circ


if __name__ == '__main__':
    n_qubit = 10
    qulacs_circ = qulacs_random_circ(n_qubit)
    state = QuantumState(n_qubit)
    qulacs_circ.update_quantum_state(state)
    qulacs_pqc = qulacs_random_pqc(n_qubit)
    ham = Observable(n_qubit)
    ham.add_operator(1, "Y 1")
    qulacs_grad_ops = GradCalculator()
    qulacs_grad_ops.calculate_grad(qulacs_pqc, ham)
    qulacs_pqc.backprop(ham)
    pqc = ParametricQuantumCircuit(1)
    pqc.add_parametric_RX_gate(0,1)
    ham = Observable(1)
    ham.add_operator(1, "Z 0")
    pqc.backprop(ham)
    qulacs_grad_ops.calculate_grad(pqc,ham)
