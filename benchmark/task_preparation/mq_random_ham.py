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


def template():
    circ = Circuit()
    circ.y(0).y(1).y(2).y(3)
    circ.barrier()
    circ.x(0).x(2)
    circ.barrier()
    circ.z(1).z(3)
    circ.barrier()
    circ.z(0).y(1).x(2).z(3)
    return circ


def mq_random_ham(n_qubit):
    qo = QubitOperator()
    for i in range(n_qubit - 3):
        qo += QubitOperator(f"Y{i} Y{i+1} Y{i+2} Y{i+3}")
        qo += QubitOperator(f"X{i} X{i+2}")
        qo += QubitOperator(f"Z{i+1} Z{i+3}")
        qo += QubitOperator(f"Z{i} Y{i+1} X{i+2} Z{i+3}")
    return qo


def mq_random_ham_prepare(backend: str, n_qubits: int):
    sim = Simulator(backend, n_qubits)
    ham = Hamiltonian(mq_random_ham(n_qubits))
    ham.get_cpp_obj()

    def run():
        sim.reset()
        sim.apply_circuit(UN(H, n_qubits))
        sim.get_expectation(ham)

    return run


if __name__ == "__main__":
    from mindquantum.core.circuit import UN
    from mindquantum.core.gates import H
    from mindquantum.core.operators import Hamiltonian
    from mindquantum.simulator import Simulator

    n_qubit = 5
    qo = mq_random_ham(n_qubit)
    sim = Simulator("mqvector", n_qubit)
    sim.apply_circuit(UN(H, n_qubit))
    ham = Hamiltonian(qo)
    e0 = sim.get_expectation(ham)
