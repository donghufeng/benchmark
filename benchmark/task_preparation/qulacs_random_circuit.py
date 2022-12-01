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
"""Generate random circuit for qulacs."""
import numpy as np
from qulacs import (
    GradCalculator,
    Observable,
    ParametricQuantumCircuit,
    QuantumCircuit,
    QuantumState,
    gate,
)
from qulacs_core import QuantumStateGpu

from benchmark import SEED
from benchmark.task_preparation import generate_random_circuit


def cy():
    return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1j], [0, 0, -1j, 0],])


def qulacs_random_circ(n_qubits):
    circ = QuantumCircuit(n_qubits)
    circ_text = generate_random_circuit(n_qubits)
    for gate_args in circ_text:
        gate: str
        gate = gate_args[0]
        if gate in ["x", "y", "z", "h", "t", "s"]:
            getattr(circ, f"add_{gate.upper()}_gate")(gate_args[1])
        elif gate == "cx":
            circ.add_CNOT_gate(gate_args[1], gate_args[2])
        elif gate == "cy":
            circ.add_dense_matrix_gate([gate_args[1], gate_args[2]], cy())
        elif gate == "cz":
            circ.add_CZ_gate(gate_args[1], gate_args[2])
        elif gate in ["rx", "ry", "rz"]:
            getattr(circ, f"add_{gate.upper()}_gate")(gate_args[1], gate_args[2])
        elif gate in ["xx", "yy", "zz"]:
            circ.add_multi_Pauli_rotation_gate(
                [gate_args[1], gate_args[2]], [ord(i) - 119 for i in gate], gate_args[3]
            )
        else:
            raise RuntimeError()
    return circ


def qulacs_random_circuit_prepare(platform: str, n_qubits: int):
    if platform == "gpu":
        QuantumState = QuantumStateGpu
    elif platform == "cpu":
        from qulacs import QuantumState
    else:
        raise RuntimeError(f"platform {platform} not supported by qulacs.")

    qulacs_circ = qulacs_random_circ(n_qubits)

    def run():
        state = QuantumState(n_qubits)
        qulacs_circ.update_quantum_state(state)
        return state

    return run


if __name__ == "__main__":
    run = qulacs_random_circuit_prepare("cpu", 5)
    run()
