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
"""Generate tc random circuit."""
from benchmark.task_preparation import generate_random_circuit

import pyqpanda as pq

def qpanda_random_circuit(qubits):
    circ_text = generate_random_circuit(len(qubits))
    prog = pq.QProg()
    for gate_args in circ_text:
        gate = gate_args[0]
        if gate in ['x', 'y', 'z', 'h', 's', 't']:
            prog.insert(getattr(pq, gate.upper())(qubits[gate_args[1]]))
        elif gate in ['cx', 'cy', 'cz']:
            prog.insert(
                getattr(pq, gate[1].upper())(qubits[gate_args[2]]).control(
                    qubits[gate_args[1]]))
        elif gate in ['rx', 'ry', 'rz']:
            prog.insert(
                getattr(pq, gate.upper())(qubits[gate_args[1]], gate_args[2]))
        elif gate in ['xx', 'yy', 'zz']:
            prog.insert(
                getattr(pq, 'R' + gate.upper())(qubits[gate_args[1]],
                                                qubits[gate_args[2]],
                                                gate_args[3]))
        else:
            raise RuntimeError(f"Error: {gate}")
    return prog


def qpanda_random_circuit_prepare(platform: str, n_qubits: int):
    if platform == "gpu":
        qvm = pq.GPUQVM()
    elif platform == "cpu":
        qvm = pq.CPUQVM()
    else:
        raise RuntimeError(f"platform {platform} not supported by pyqpanda.")
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n_qubits)
    prog = qpanda_random_circuit(qubits)

    def run():
        qvm.directly_run(prog)
        return qvm.get_qstate()

    return run


if __name__ == "__main__":
    run = qpanda_random_circuit_prepare("cpu", 5)
    run()
