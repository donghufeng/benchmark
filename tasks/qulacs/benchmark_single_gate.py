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
"""Benchmark a single gate."""
import argparse

from qulacs import QuantumCircuit
from benchmark import Benchmark

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--file-name", help="file name", type=str, default="0001")
parser.add_argument("-f", "--file-dir", help="file dir", type=str, default="./")
parser.add_argument("-p", "--platform", help="platform", type=str, default="cpu")
parser.add_argument("-q", "--qubit", help="number of qubit", type=int, default=4)
parser.add_argument("-g", "--gate", help="which gate you want to benchmark.", type=str, default='X')
args = parser.parse_args()

def generate_model(platform:str,n_qubits:int, gate:str):
    if platform == 'cpu':
        from qulacs import QuantumState
    elif platform == 'gpu':
        from qulacs_core import QuantumStateGpu as QuantumState
    else:
        raise RuntimeError(f"Unknown backend: {platform}")
    sim = QuantumState(n_qubits)
    circ = QuantumCircuit(n_qubits)
    if gate == 'H':
        circ.add_H_gate(3)
    elif gate == 'X':
        circ.add_X_gate(3)
    elif gate == 'T':
        circ.add_T_gate(3)
    elif gate == 'RX':
        circ.add_RX_gate(3, 1.23)
    elif gate == 'RZ':
        circ.add_RZ_gate(3, 1.23)
    elif gate == 'CNOT':
        circ.add_CNOT_gate(2, 3)
    else:
        raise RuntimeError(f"We do not benchmark {gate}")
    return sim, circ

def test_single_gate(platform:str, n_qubits:int):
    cpp_sim, cpp_circ = generate_model(platform, n_qubits, args.gate)
    Benchmark(
        args.file_name,
        args.file_dir,
        f"single_gate_{args.gate}",
        {
            "framework": "qulacs",
            "platform": platform,
            "n_qubit": n_qubits,
        },
        cpp_circ.update_quantum_state,
        cpp_sim,
        warmup=True,
    )
test_single_gate(args.platform, args.qubit)
