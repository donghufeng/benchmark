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
"""Generate 4 regular model."""

# NOT GRADIENT BASED.

import networkx as nx
import numpy as np
import pyqpanda as pq

from benchmark import SEED


def qpanda_qaoa_prepare(platform: str, n_qubit):
    if platform == "gpu":
        qvm = pq.init_quantum_machine(pq.QMachineType.GPU)
    elif platform == "cpu":
        qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
    else:
        raise RuntimeError(f"platform {platform} not supported by pyqpanda.")
    qubits = qvm.qAlloc_many(n_qubit)

    net = nx.random_regular_graph(4, n_qubit, SEED)
    edges = list(net.edges)
    p0 = pq.var(
        np.random.uniform(-1, 1, len(edges) + n_qubit).astype(np.float64)[:, None], True
    )

    circ = pq.VariationalQuantumCircuit()
    for i in qubits:
        circ.insert(pq.VariationalQuantumGate_H(i))
    for idx, (i, j) in enumerate(edges):
        circ.insert(pq.VariationalQuantumGate_CNOT(qubits[i], qubits[j]))
        circ.insert(pq.VariationalQuantumGate_RZ(qubits[j], p0[idx]))
        circ.insert(pq.VariationalQuantumGate_CNOT(qubits[i], qubits[j]))
    for i in range(n_qubit):
        circ.insert(pq.VariationalQuantumGate_RX(qubits[i], p0[idx + 1 + i]))
    op = {}
    for i, j in edges:
        op[f"Z{i} Z{j}"] = 1
    hp = pq.PauliOperator(op)

    loss = pq.qop(circ, hp, qvm, qubits)
    optimizer = pq.MomentumOptimizer.minimize(loss, 0.01, 0.8)
    leaves = optimizer.get_variables()

    def run():
        optimizer.run(leaves, 0)
        loss_value = optimizer.get_loss()
        return loss_value

    return run


if __name__ == "__main__":
    import numpy as np

    n_qubit = 5
    run = qpanda_qaoa_prepare("cpu", n_qubit)
    run()
