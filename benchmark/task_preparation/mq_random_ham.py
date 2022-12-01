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
"""Generate random hamiltonian."""

from mindquantum.core.circuit import UN, Circuit
from mindquantum.core.gates import H
from mindquantum.core.operators import Hamiltonian, QubitOperator
from mindquantum.simulator import Simulator

from benchmark.task_preparation import generate_random_ham


def mq_random_ham(n_qubit):
    qo = QubitOperator()
    ham_text = generate_random_ham(n_qubit)
    for term in ham_text:
        qo += QubitOperator(" ".join(f"{i}{j}" for i, j in term))
    return qo


def mq_random_ham_prepare(backend: str, n_qubits: int):
    sim = Simulator(backend, n_qubits)
    ham = Hamiltonian(mq_random_ham(n_qubits))
    ham.get_cpp_obj()

    def run():
        sim.reset()
        sim.apply_circuit(UN(H, n_qubits))
        return sim.get_expectation(ham)

    return run


if __name__ == "__main__":
    run = mq_random_ham_prepare("mqvector", 4)
    run()
