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

from benchmark import SEED
import networkx as nx

from mindquantum.algorithm.nisq.qaoa import MaxCutAnsatz
from mindquantum.simulator import Simulator
from mindquantum.core.operators import Hamiltonian


def mq_qaoa_exp(n_qubit, backend):
    net = nx.random_regular_graph(2, n_qubit, SEED)
    edges = list(net.edges)
    maxcut = MaxCutAnsatz(edges)
    circ = maxcut.circuit
    sim = Simulator(backend, circ.n_qubits)
    ham = Hamiltonian(maxcut.hamiltonian)
    return sim.get_expectation_with_grad(ham, circ), len(circ.params_name)


if __name__ == '__main__':
    import numpy as np

    grad_ops, n_p = mq_qaoa_exp(5, 'mqvector')
    p0 = np.random.uniform(-1, 1, n_p)
    f, g = grad_ops(p0)
