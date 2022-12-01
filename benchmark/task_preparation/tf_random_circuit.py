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
import numpy as np
import sympy

from benchmark.task_preparation import generate_random_circuit


def tf_random_circuit(n_qubit):
    import cirq

    qubits = cirq.GridQubit.rect(1, n_qubit)
    circ = cirq.Circuit()
    circ_text = generate_random_circuit(n_qubit)
    for gate_args in circ_text:
        gate = gate_args[0]
        gate: str
        if gate in ["x", "y", "z", "h", "s", "t"]:
            circ += getattr(cirq, gate.upper())(qubits[gate_args[1]])
        elif gate in ["cx", "cz"]:
            circ += getattr(cirq, gate.upper())(
                qubits[gate_args[1]], qubits[gate_args[2]]
            )
        elif gate == "cy":
            circ += cirq.Y(qubits[gate_args[2]]).controlled_by(qubits[gate_args[1]])
        elif gate in ["rx", "ry", "rz"]:
            circ += getattr(cirq, f"R{gate[-1]}")(rads=gate_args[2]).on(
                qubits[gate_args[1]]
            )
        elif gate in ["xx", "yy", "zz"]:
            circ += (
                getattr(cirq, gate.upper())(qubits[gate_args[1]], qubits[gate_args[2]])
                ** gate_args[3]
            )
        else:
            raise RuntimeError()
    return circ


def tf_random_circuit_prepare(platform: str, n_qubits: int):
    import os

    if platform == "gpu":
        import tensorflow as tf

        gpu = tf.config.list_physical_devices("GPU")
        tf.config.experimental.set_memory_growth(device=gpu[0], enable=True)
    elif platform == "cpu":
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    else:
        raise RuntimeError(
            f"Platform {platform} for tf_random_circuit_prepare unrecognized, should be cpu or gpu."
        )
    from tensorflow_quantum.core.ops import tfq_simulate_ops
    from tensorflow_quantum.core.serialize.serializer import serialize_circuit

    circ = tf_random_circuit(n_qubits)
    circ = str(serialize_circuit(circ))

    def run():
        return tfq_simulate_ops.tfq_simulate_state([circ], [], [[]])

    return run


if __name__ == "__main__":
    run = tf_random_circuit_prepare("cpu", 5)
    run()
