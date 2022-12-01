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
"""Generate random hamiltonian."""

import numpy as np

from benchmark import SEED

PAULI_LIST = ["X", "Y", "Z"]


def generate_random_ham(n_qubits: int):
    """
    Generate random hamiltonian.

    Examples:
        [
            [['X', 0], ['Y', 1]],
            [['Z', 1]],
            [['Z', 0], ['X', 2]]
        ]
    """
    if n_qubits < 4 or n_qubits > 24:
        raise ValueError("We only benchmark 4-24 qubits random hamiltonian.")
    n_terms = 48 * (4 - n_qubits) + 1000
    np.random.seed(SEED)
    qubit_idx = list(range(n_qubits))
    out = []
    for _ in range(n_terms):
        np.random.shuffle(qubit_idx)
        n_pauli = np.random.randint(n_qubits) + 1
        term = []
        for i in range(n_pauli):
            term.append(
                [PAULI_LIST[np.random.choice(len(PAULI_LIST), 1)[0]], qubit_idx[i]]
            )
        out.append(term)
    return out


if __name__ == "__main__":
    ham = generate_random_ham(5)
