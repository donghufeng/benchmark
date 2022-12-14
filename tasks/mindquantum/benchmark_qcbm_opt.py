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

from mindquantum.core.circuit import Circuit
from mindquantum.core.gates import BasicGate, H, X, T, RX, RZ
from mindquantum.simulator import Simulator
from mindquantum.algorithm.compiler.circuit_opt import grouping
from benchmark import Benchmark
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-n",
                    "--file-name",
                    help="file name",
                    type=str,
                    default="0001")
parser.add_argument("-f",
                    "--file-dir",
                    help="file dir",
                    type=str,
                    default="./")
parser.add_argument("-p",
                    "--platform",
                    help="platform",
                    type=str,
                    default="cpu")
parser.add_argument("-q",
                    "--qubit",
                    help="number of qubit",
                    type=int,
                    default=4)
args = parser.parse_args()


def first_rotation(circuit: Circuit, nqubits: int):
    for k in range(nqubits):
        circuit += RX(np.random.rand()).on(k)
        circuit += RZ(np.random.rand()).on(k)


def mid_rotation(circuit: Circuit, nqubits: int):
    for k in range(nqubits):
        circuit += RZ(np.random.rand()).on(k)
        circuit += RX(np.random.rand()).on(k)
        circuit += RZ(np.random.rand()).on(k)


def last_rotation(circuit: Circuit, nqubits: int):
    for k in range(nqubits):
        circuit += RZ(np.random.rand()).on(k)
        circuit += RX(np.random.rand()).on(k)


def entangler(circuit: Circuit, nqubits, pairs):
    for a, b in pairs:
        circuit += X.on(b, a)


def build_circuit(nqubits, depth, pairs) -> Circuit:
    circuit = Circuit()
    first_rotation(circuit, nqubits)
    entangler(circuit, nqubits, pairs)
    for k in range(depth):
        mid_rotation(circuit, nqubits)
        entangler(circuit, nqubits, pairs)

    last_rotation(circuit, nqubits)
    return circuit


def generate_model(platform: str, n_qubits: int):
    if platform == 'cpu':
        backend = 'mqvector'
    elif platform == 'gpu':
        backend = 'mqvector_gpu'
    else:
        raise RuntimeError(f"Unknown backend: {platform}")
    sim = Simulator(backend, n_qubits)
    pairs = [(i, (i + 1) % n_qubits) for i in range(n_qubits)]
    circ = build_circuit(n_qubits, 9, pairs)
    circ = grouping(circ, 3)
    return sim.backend.sim, circ.get_cpp_obj()


def test_QCBM(platform: str, n_qubits: int):
    cpp_sim, cpp_circ = generate_model(platform, n_qubits)
    Benchmark(
        args.file_name,
        args.file_dir,
        f"QCBM",
        {
            "framework": "mindquantum_opt",
            "platform": platform,
            "n_qubit": n_qubits,
        },
        cpp_sim.apply_circuit,
        cpp_circ,
        warmup=True,
    )


test_QCBM(args.platform, args.qubit)
