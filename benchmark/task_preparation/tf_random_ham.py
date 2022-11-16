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
"tensorflow random quantum ham"

import cirq


def tf_random_ham(n_qubit):
    qubits = cirq.GridQubit.rect(1, n_qubit)
    qo = 0
    for i in range(n_qubit - 3):
        qo += cirq.Y(qubits[i]) * cirq.Y(qubits[i + 1]) * cirq.Y(
            qubits[i + 2]) * cirq.Y(qubits[i + 3])
        qo += cirq.X(qubits[i]) * cirq.X(qubits[i + 2])
        qo += cirq.Z(qubits[i + 1]) * cirq.Z(qubits[i + 3])
        qo += cirq.Z(qubits[i]) * cirq.Y(qubits[i + 1]) * cirq.X(
            qubits[i + 2]) * cirq.Z(qubits[i + 3])
    return qo, qubits


if __name__ == '__main__':
    ham, qubits = tf_random_ham(5)
