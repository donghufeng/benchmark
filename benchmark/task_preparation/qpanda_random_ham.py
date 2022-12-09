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
"""Benchmark random hamiltonian expectation on qpanda."""
import pyqpanda as pq

from benchmark.task_preparation import generate_random_ham


def trans_ham(n_qubits: int):
    ham_text = generate_random_ham(n_qubits)
    out = pq.PauliOperator()
    for i in ham_text:
        out += pq.PauliOperator(" ".join([f"{t[0]}{t[1]}" for t in i]), 1)
    return out.to_hamiltonian(1)


def qpanda_random_ham_prepare(platform: str, n_qubits: int):
    if platform == "gpu":
        qvm = pq.GPUQVM()
    elif platform == "cpu":
        qvm = pq.CPUQVM()
    else:
        raise RuntimeError(f"platform {platform} not supported by pyqpanda.")
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n_qubits)
    prog = pq.QProg()
    for i in range(n_qubits):
        prog.insert(pq.H(qubits[i]))

    ham = trans_ham(n_qubits)

    def run():
        return qvm.get_expectation(prog, ham, qubits)

    return run


if __name__ == "__main__":
    run = qpanda_random_ham_prepare("cpu", 5)
    print(run())
