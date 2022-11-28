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


def tf_random_ham(n_qubit):
    import cirq

    qubits = cirq.GridQubit.rect(1, n_qubit)
    qo = 0
    for i in range(n_qubit - 3):
        qo += (
            cirq.Y(qubits[i])
            * cirq.Y(qubits[i + 1])
            * cirq.Y(qubits[i + 2])
            * cirq.Y(qubits[i + 3])
        )
        qo += cirq.X(qubits[i]) * cirq.X(qubits[i + 2])
        qo += cirq.Z(qubits[i + 1]) * cirq.Z(qubits[i + 3])
        qo += (
            cirq.Z(qubits[i])
            * cirq.Y(qubits[i + 1])
            * cirq.X(qubits[i + 2])
            * cirq.Z(qubits[i + 3])
        )
    return qo, qubits


def tf_random_ham_prepare(platform: str, n_qubits: int):
    import os

    if platform == "gpu":
        import tensorflow as tf

        gpu = tf.config.list_physical_devices("GPU")
        tf.config.experimental.set_memory_growth(device=gpu[0], enable=True)
    elif platform == "cpu":
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    else:
        raise RuntimeError(
            f"Platform {platform} for tf_random_ham_prepare unrecognized, should be cpu or gpu."
        )
    import cirq
    import tensorflow_quantum as tfq
    from tensorflow_quantum.python import util

    ham, qubits = tf_random_ham(n_qubits)
    my_op = tfq.get_expectation_op()
    circ = cirq.Circuit()
    for i in qubits:
        circ += cirq.H(i)
    my_circuit_tensor = util.convert_to_tensor([circ])
    my_paulis = util.convert_to_tensor([[ham]])

    def run():
        return my_op(my_circuit_tensor, [], [[]], my_paulis)

    return run


if __name__ == "__main__":
    run = tf_random_ham_prepare("cpu", 5)
    run()
