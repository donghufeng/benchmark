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
"""Benchmark maxcut with paddle quantum."""
import networkx as nx

from benchmark import SEED


def paddle_qaoa_prepare(platform: str, n_qubits: int):
    import paddle
    import paddle_quantum as pdq

    if platform == "cpu":
        paddle.device.set_device("cpu")
    elif platform == "gpu":
        paddle.device.set_device("gpu:0")
    else:
        raise ValueError(f"platform {platform} is not supported for paddle quantum.")
    net = nx.random_regular_graph(4, n_qubits, SEED)
    edges = list(net.edges)
    circ = pdq.ansatz.Circuit(n_qubits)
    node = []
    for i, j in edges:
        if i not in node:
            node.append(i)
        if j not in node:
            node.append(j)
    circ.qaoa_layer(edges, node)
    ham = []
    for i, j in edges:
        ham.append([1, f"z{i},z{j}"])
    loss_func = pdq.loss.ExpecVal(pdq.Hamiltonian(ham))

    def run():
        state = circ()
        loss = loss_func(state)
        loss.backward()
        return loss.numpy()

    return run


if __name__ == "__main__":
    run = paddle_qaoa_prepare("cpu", 5)
    run()
