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
"""Benchmark random circuit evolution on qiskit."""
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

from benchmark.task_preparation import generate_random_circuit


def prepare_circuit(n_qubits: int):
    circ_text = generate_random_circuit(n_qubits)
    circ = QuantumCircuit(n_qubits)
    for gate_args in circ_text:
        gate = gate_args[0]
        if gate in ["x", "y", "z", "h", "s", "t"]:
            getattr(circ, gate)(gate_args[1])
        elif gate in ["cx", "cy", "cz"]:
            getattr(circ, gate)(gate_args[1], gate_args[2])
        elif gate in ["rx", "ry", "rz"]:
            getattr(circ, gate)(gate_args[2], gate_args[1])
        elif gate in ["xx", "yy", "zz"]:
            getattr(circ, "r" + gate)(gate_args[3], gate_args[1], gate_args[2])
        else:
            raise RuntimeError(f"{gate}")
    return circ


def qiskit_random_circuit_prepare(platform: str, n_qubits: int):
    if platform == "cpu":
        Simulator = AerSimulator(method="statevector", device="CPU")
    elif platform == "gpu":
        Simulator = AerSimulator(method="statevector", device="GPU")
    else:
        raise RuntimeError("qiskit do not support platform " + platform)
    circ = prepare_circuit(n_qubits)
    circ.save_statevector()

    def run():
        return Simulator.run(circ).result().get_statevector(circ)

    return run


if __name__ == "__main__":
    run = qiskit_random_circuit_prepare("gpu", 5)
    run()
