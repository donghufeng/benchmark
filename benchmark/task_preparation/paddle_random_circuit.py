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
"""Benchmark random quantum circuit evolution with paddle quantum."""
from benchmark.task_preparation import generate_random_circuit


def paddle_random_circuit(n_qubits: int):
    import paddle_quantum as pdq

    circ_text = generate_random_circuit(n_qubits)
    circ = pdq.ansatz.Circuit(n_qubits)
    for gate_args in circ_text:
        gate = gate_args[0]
        if gate in ["x", "y", "z", "h", "s", "t"]:
            getattr(circ, gate)(gate_args[1])
        elif gate in ["cx", "cy", "cz"]:
            getattr(circ, gate)([gate_args[1], gate_args[2]])
        elif gate in ["rx", "ry", "rz"]:
            getattr(circ, gate)(gate_args[1], gate_args[2])
        elif gate in ["xx", "yy", "zz"]:
            getattr(circ, "r" + gate)([gate_args[1], gate_args[2]])
        else:
            raise RuntimeError()
    return circ


def paddle_random_circuit_prepare(platform: str, n_qubits: int):
    import numpy as np
    import paddle

    if platform == "cpu":
        paddle.device.set_device("cpu")
    elif platform == "gpu":
        paddle.device.set_device("gpu:0")
    else:
        raise ValueError(f"platform {platform} is not supported for paddle quantum.")
    circ = paddle_random_circuit(n_qubits)

    def run():
        qs = circ.forward()
        return qs

    return run


if __name__ == "__main__":
    import numpy as np

    n_qubits = 5
    run = paddle_random_circuit_prepare("cpu", n_qubits)
    run()
