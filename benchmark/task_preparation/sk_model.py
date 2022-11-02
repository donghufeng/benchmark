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
"""Generate sk model."""
from typing import Tuple, List

from mindquantum.algorithm.nisq.qaoa import MaxCutAnsatz
from mindquantum.core.operators import QubitOperator
from mindquantum.core.circuit import Circuit
from benchmark import get_config, get_y, SEED


def generate_sk_edges(n: int) -> List[Tuple[int, int]]:
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            edges.append((i, j))
    return edges


def generate_sk_model(n_qubits: int) -> Tuple[Circuit, QubitOperator]:
    task_name = 'maxcut_sk_model_with_qaoa'
    config = get_config(task_name)
    qubit_max = config['qubit_max']
    qubit_min = config['qubit_min']
    layer_max = config['layer_max']
    layer_min = config['layer_min']
    if not (qubit_min <= n_qubits <= qubit_max):
        raise ValueError(
            f"for {task_name}, qubits should be in [{qubit_min}, {qubit_max}]")
    layer_num = get_y(n_qubits, qubit_max, layer_min, qubit_min, layer_max)
    nodes = generate_sk_edges(n_qubits)
    maxcut = MaxCutAnsatz(nodes, layer_num)
    return maxcut.circuit, maxcut.hamiltonian
