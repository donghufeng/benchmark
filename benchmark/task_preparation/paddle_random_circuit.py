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


def paddle_random_circuit(n_qubits: int, params):
    import paddle_quantum as pdq

    circ = pdq.ansatz.Circuit(n_qubits)
    for i in range(n_qubits - 3):
        circ.h([i, i + 1, i + 2, i + 3])
        circ.rx(i, param=params[i * 11])
        circ.rx(i + 1, param=params[i * 11 + 1])
        circ.rx(i + 2, param=params[i * 11 + 2])
        circ.rx(i + 3, param=params[i * 11 + 3])
        circ.crx([i, i + 1])
        circ.crx([i + 1, i + 2])
        circ.crx([i + 2, i + 3])
        circ.crx([i + 3, i])
        circ.rxx([i, i + 1], param=params[i * 11 + 4])
        circ.ryy([i + 1, i + 2], param=params[i * 11 + 5])
        circ.rzz([i + 2, i + 3], param=params[i * 11 + 6])
        circ.s(i)
        circ.s(i + 1)
        circ.t(i + 3)
        circ.t(i + 2)
        circ.cp([i, i + 1], param=params[i * 11 + 7])
        circ.cp([i, i + 1], param=params[i * 11 + 8])
        circ.swap([i, i + 3])
        circ.cp([i + 1, i], param=params[i * 11 + 9])
        circ.cp([i + 2, i + 3], param=params[i * 11 + 10])
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
    p0 = np.random.uniform(-1, 1, (n_qubits - 2) * 11)
    circ = paddle_random_circuit(n_qubits, p0)

    def run():
        qs = circ.forward()
        return qs

    return run


if __name__ == "__main__":
    import numpy as np

    n_qubits = 5
    p0 = np.random.uniform(-1, 1, (n_qubits - 2) * 11)
    circ = paddle_random_circuit(5, p0)
    qs = circ.forward()
