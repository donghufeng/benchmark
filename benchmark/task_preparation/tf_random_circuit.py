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
"tensorflow random quantum circuit"

import cirq


def tf_random_circuit(n_qubit):

    def c_fun(params):
        qubits = cirq.GridQubit.rect(1, n_qubit)
        circ = cirq.Circuit()
        for i in range(n_qubit - 3):
            circ += cirq.H(qubits[i])
            circ += cirq.H(qubits[i + 1])
            circ += cirq.H(qubits[i + 2])
            circ += cirq.H(qubits[i + 3])
            circ += cirq.Rx(rads=params[i * 11]).on(qubits[i])
            circ += cirq.Rx(rads=params[i * 11 + 1]).on(qubits[i + 1])
            circ += cirq.Rx(rads=params[i * 11 + 2]).on(qubits[i + 2])
            circ += cirq.Rx(rads=params[i * 11 + 3]).on(qubits[i + 3])
            circ += cirq.CX(qubits[i], qubits[i + 1])
            circ += cirq.CX(qubits[i + 1], qubits[i + 2])
            circ += cirq.CX(qubits[i + 2], qubits[i + 3])
            circ += cirq.CX(qubits[i + 3], qubits[i])
            circ += cirq.XX(qubits[i], qubits[i + 1])**params[i * 11 + 4]
            circ += cirq.YY(qubits[i + 1], qubits[i + 2])**params[i * 11 + 5]
            circ += cirq.ZZ(qubits[i + 2], qubits[i + 3])**params[i * 11 + 6]
            circ += cirq.S(qubits[i])
            circ += cirq.S(qubits[i + 1])
            circ += cirq.T(qubits[i + 2])
            circ += cirq.T(qubits[i + 3])
            circ += cirq.cphase(rads=params[i * 11 + 7]).on(
                qubits[i], qubits[i + 1])
            circ += cirq.cphase(rads=params[i * 11 + 8]).on(
                qubits[i + 3], qubits[i + 2])
            circ += cirq.SWAP(qubits[i], qubits[i + 3])
            circ += cirq.CXPowGate().on(qubits[i],
                                        qubits[i + 1])**params[i * 11 + 9]
            circ += cirq.CXPowGate().on(qubits[i + 2],
                                        qubits[i + 3])**params[i * 11 + 10]
        return circ, qubits

    return c_fun


if __name__ == '__main__':
    import numpy as np
    import sympy
    from tensorflow_quantum.python import util
    from tensorflow_quantum.core.ops import tfq_simulate_ops
    from tensorflow_quantum.core.serialize.serializer import serialize_circuit
    p = [f"p{i}" for i in range(2 * 11)]
    p = sympy.symbols(' '.join(p))
    p0 = np.random.uniform(-1, 1, 2 * 11)
    circ, qubits = tf_random_circuit(5)(p)
    tfq_simulate_ops.tfq_simulate_state([str(serialize_circuit(circ))],
                                        [str(i) for i in p], [p0])
    # ham = cirq.PauliSum.from_pauli_strings(cirq.PauliString(1, cirq.Y(qubits[1])))
    ham = cirq.Y(qubits[1])
    ham_tensor=util.convert_to_tensor([[ham]])
    tfq_simulate_ops.tfq_simulate_expectation([str(serialize_circuit(circ))],
                                              [str(i) for i in p], [p0], ham_tensor)
