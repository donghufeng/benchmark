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
"""Generate random circuit."""

from mindquantum.utils import random_circuit
from benchmark import get_config, get_y, SEED


def generate_random_circuit(n_qubits):
    task_name = 'random_circuit_qs'
    config = get_config(task_name)
    qubit_max = config['qubit_max']
    qubit_min = config['qubit_min']
    gate_num_max = config['gate_num_max']
    gate_num_min = config['gate_num_min']
    if not (qubit_min<=n_qubits<=qubit_max):
        raise ValueError(f"for {task_name}, qubits should be in [{qubit_min}, {qubit_max}]")
    gate_num = get_y(n_qubits, qubit_max, gate_num_min, qubit_min, gate_num_max)
    return random_circuit(n_qubits, gate_num, seed=SEED)
