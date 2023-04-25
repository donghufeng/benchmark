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

import networkx as nx
import numpy as np
from qulacs import Observable, ParametricQuantumCircuit
from qulacs.circuit import QuantumCircuitOptimizer
from mindquantum.algorithm.nisq.qaoa import MaxCutAnsatz
from benchmark import SEED
from benchmark.translator.qulacs import mq_circ_to_qulacs,mq_qubit_ops_to_qulacs
def maxcut_circ(n_qubit):
    net = nx.random_regular_graph(4, n_qubit, SEED)
    edges = list(net.edges)
    maxcut = MaxCutAnsatz(edges)
    circ =mq_circ_to_qulacs(maxcut.circuit)
    ham = mq_qubit_ops_to_qulacs(maxcut.hamiltonian)
    return circ, ham

def qulacs_qaoa_prepare(platform: str, n_qubit):
    if platform == "gpu":
        raise RuntimeError("Qulacs qaoa does not support gpu.")
    elif platform == "cpu":
        from qulacs import QuantumState
    else:
        raise RuntimeError(f"platform {platform} not supported by qulacs.")
    circ, op = maxcut_circ(n_qubit)
    n_p = circ.get_parameter_count()
    p0 = np.random.uniform(-1, 1, n_p)

    def run():
        for i in range(n_p):
            circ.set_parameter(i, p0[i])
        return circ.backprop(op)

    return run
