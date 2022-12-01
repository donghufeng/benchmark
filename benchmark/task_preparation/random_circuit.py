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
"""Generate random circuit in text form."""
import numpy as np

from benchmark import SEED

GATE_LIST = [
    "x",
    "y",
    "z",
    "h",
    "s",
    "t",
    "cx",
    "cy",
    "cz",
    "rx",
    "ry",
    "rz",
    "xx",
    "yy",
    "zz",
]


def generate_random_circuit(n_qubits: int):
    """
    Generate random circuit.

    Possible case is:
        ['x', 0]           -> X.on(0)
        ['cx', 0, 1]       -> X.on(1, 0)
        ['rx', 0, 1.2]     -> RX(1.2).on(0)
        ['xx', 0, 1, 1.2]  -> XX(1.2).on([0, 1])
    """
    if n_qubits < 4 or n_qubits > 24:
        raise ValueError("We only benchmark 4-24 qubits random circuit.")
    n_gates = 40 * (4 - n_qubits) + 1000
    np.random.seed(SEED)
    gate_poi = np.random.randint(0, len(GATE_LIST), n_gates)
    gates = []
    for i in gate_poi:
        gate = GATE_LIST[i]
        poi_maybe = list(range(n_qubits))
        np.random.shuffle(poi_maybe)
        coeff_maybe = np.random.uniform(-np.pi, np.pi)
        if gate in ["x", "y", "z", "h", "s", "t"]:
            gates.append([gate, poi_maybe[0]])
        elif gate in ["cx", "cy", "cz"]:
            gates.append([gate, poi_maybe[0], poi_maybe[1]])
        elif gate in ["rx", "ry", "rz"]:
            gates.append([gate, poi_maybe[0], coeff_maybe])
        elif gate in ["xx", "yy", "zz"]:
            gates.append([gate, poi_maybe[0], poi_maybe[1], coeff_maybe])
        else:
            raise ValueError(f"gate {gate} will not be benchmarked.")
    return gates


if __name__ == "__main__":
    circ = generate_random_circuit(24)
