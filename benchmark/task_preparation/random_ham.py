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
"""Generate random hamiltonian."""

import numpy as np

from mindquantum.core.operators import QubitOperator
from benchmark import get_config, get_y, SEED


def random_ham(n_qubits: int) -> QubitOperator:
    np.random.seed(SEED)
    task_name = 'apply_random_hamiltonian'
    config = get_config(task_name)
    qubit_max = config['qubit_max']
    qubit_min = config['qubit_min']
    ham_term_max = config['ham_term_max']
    ham_term_min = config['ham_term_min']
    if not (qubit_min <= n_qubits <= qubit_max):
        raise ValueError(
            f"for {task_name}, qubits should be in [{qubit_min}, {qubit_max}]")
    n_terms = min(
        get_y(n_qubits, qubit_max, ham_term_min, qubit_min, ham_term_max),
        4**n_qubits)
    if n_qubits < 10:
        all_terms = ['I', 'X', 'Y', 'Z']
        for i in range(n_qubits - 1):
            all_terms = [i + j for i in all_terms for j in ['I', 'X', 'Y', 'Z']]
        np.random.shuffle(all_terms)
        terms = all_terms[:(min(len(all_terms), n_terms))]
    else:
        terms = set()
        while True:
            term = ''
            for i in range(n_qubits):
                tmp = ['I', 'X', 'Y', 'Z']
                np.random.shuffle(tmp)
                term += tmp[0]
            terms.add(term)
            if len(terms) >= n_terms:
                break
    op = QubitOperator()

    def fun(i, j):
        return i != 'I' and f'{i}{j}'

    for i in terms:
        assert len(i) == n_qubits
        term = ' '.join([
            f'{n}{idx}' for (n, idx) in filter(
                lambda n_idx: n_idx[0] != 'I' and f'{n_idx[0]}{n_idx[1]}',
                zip(i, range(len(i))))
        ])
        op += QubitOperator(term, float(np.random.uniform(-2, 2, 1)))
    return op
