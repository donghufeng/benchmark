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
"""Generate 2 regular model."""

import networkx as nx
import numpy as np
from qulacs import Observable, ParametricQuantumCircuit
from qulacs.circuit import QuantumCircuitOptimizer

from benchmark import SEED


def qulacs_qaoa_prepare(platform: str, n_qubit):
    if platform == "gpu":
        from qulacs_core import QuantumStateGpu as QuantumState
    elif platform == "cpu":
        from qulacs import QuantumState
    else:
        raise RuntimeError(f"platform {platform} not supported by qulacs.")
    net = nx.random_regular_graph(2, n_qubit, SEED)
    edges = list(net.edges)
    p0 = np.random.uniform(-1, 1, len(edges) + n_qubit)

    circ = ParametricQuantumCircuit(n_qubit)
    for i in range(n_qubit):
        circ.add_H_gate(i)
    for idx, (i, j) in enumerate(edges):
        circ.add_parametric_multi_Pauli_rotation_gate([i, j], [3, 3], p0[idx])
    for i in range(n_qubit):
        circ.add_parametric_RX_gate(i, p0[idx + 1 + i])
    op = Observable(n_qubit)
    for i, j in edges:
        op.add_operator(1, f"Z {i} Z {j}")
    n_p = len(edges) + n_qubit
    QuantumCircuitOptimizer().optimize(circ, 1)
    p0 = np.random.uniform(-1, 1, n_p)

    def run():
        for i in range(n_p):
            circ.set_parameter(i, p0[i])
        return circ.backprop(op)

    return run


if __name__ == "__main__":
    import numpy as np

    run = qulacs_qaoa_prepare(5)
    run()
