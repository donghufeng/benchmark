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
"""Generate mq random circuit."""

from mindquantum.core import gates as G
from mindquantum.core.circuit import Circuit
from mindquantum.simulator import Simulator
from mindquantum.algorithm.compiler.circuit_opt import grouping
from benchmark.task_preparation import generate_random_circuit


def mq_random_circuit(n_qubits: int):
    circ_text = generate_random_circuit(n_qubits)
    circ = Circuit()
    for gate_args in circ_text:
        gate = gate_args[0]
        if gate in ["x", "y", "z", "h", "s", "t"]:
            circ += getattr(G, gate.upper()).on(gate_args[1])
        elif gate in ["cx", "cy", "cz"]:
            circ += getattr(G, gate[-1].upper()).on(gate_args[2], gate_args[1])
        elif gate in ["rx", "ry", "rz"]:
            circ += getattr(G, gate.upper())(gate_args[2]).on(gate_args[1])
        elif gate in ["xx", "yy", "zz"]:
            circ += getattr(G, gate.upper())(gate_args[3]).on(
                [gate_args[1], gate_args[2]]
            )
        else:
            raise RuntimeError()
    return circ


def mq_random_circuit_prepare(backend: str, n_qubits: str, group=False):
    circ = mq_random_circuit(n_qubits)
    if group:
        circ = grouping(circ, 3)
    sim = Simulator(backend, n_qubits)
    circ.get_cpp_obj()

    def run():
        sim.reset()
        sim.apply_circuit(circ)
        return sim

    return run


if __name__ == "__main__":
    run = mq_random_circuit_prepare("mqvector", 10)
