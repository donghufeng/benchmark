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
"""Benchmark expectation of random hamiltonian."""


def paddle_random_ham_prepare(platform: str, n_qubits: int):
    import paddle

    if platform == "cpu":
        paddle.device.set_device("cpu")
    elif platform == "gpu":
        paddle.device.set_device("gpu:0")
    else:
        raise ValueError(f"platform {platform} is not supported for paddle quantum.")
    import paddle_quantum as pdq

    H_D_list = []
    for i in range(n_qubits - 3):
        H_D_list.append([1.0, f"y{i},y{i+1},y{i+2},y{i+3}"])
        H_D_list.append([1.0, f"x{i},x{i+2}"])
        H_D_list.append([1.0, f"z{i+1},z{i+3}"])
        H_D_list.append([1.0, f"z{i},y{i+1},x{i+2},z{i+3}"])
    ham = pdq.Hamiltonian(H_D_list)
    exp = pdq.loss.ExpecVal(ham)
    circ = pdq.ansatz.Circuit(n_qubits)
    circ.h(range(n_qubits))

    def run():
        return exp(circ.forward())

    return run


if __name__ == "__main__":
    n_qubits = 5
    run = paddle_random_ham_prepare("cpu", n_qubits)
    run()
