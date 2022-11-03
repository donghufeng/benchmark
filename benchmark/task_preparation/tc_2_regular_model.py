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

import tensorcircuit as tc


def tc_qaoa_exp(n_qubit):
    net = nx.random_regular_graph(2, n_qubit, SEED)
    edges = list(net.edges)

    def c_fun(p):
        circ = tc.Circuit(n_qubit)
        for i in range(n_qubit):
            circ.h(i)
        for idx, (i, j) in enumerate(edges):
            circ.rzz(i, j, theta=p[idx])
        for i in range(n_qubit):
            circ.rx(i, theta=p[idx + i + 1])
        return circ

    def energy(p):
        circ = c_fun(p)
        e0 = 0.0
        for i, j in edges:
            e0 += circ.expectation((tc.gates.z(), [i]), (tc.gates.z(), [j]))
        return tc.backend.real(e0)

    return energy, len(edges) + n_qubit


if __name__ == '__main__':
    import numpy as np
    tc.set_backend('tensorflow')
    tc.set_dtype('complex128')

    energy, n_p = tc_qaoa_exp(5)
    p0 = tc.backend.cast(np.random.uniform(-1, 1, n_p), 'float64')
    g = tc.backend.value_and_grad(energy)
    g = tc.backend.jit(g)
    g(p0)
