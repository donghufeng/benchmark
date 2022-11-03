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

import numpy as np

from mindquantum.core.circuit import Circuit, UN, add_prefix, shift
from mindquantum.core.gates import (
    H,
    RX,
    X,
    T,
    S,
    PhaseShift,
    XX,
    YY,
    ZZ,
    BARRIER,
    UnivMathGate,
    SWAP,
)
from benchmark import SEED


def random_circuit_template():
    circ = Circuit()
    circ += UN(H, range(4))
    circ += Circuit([RX(f"p{i}").on(i) for i in range(4)])
    circ += Circuit([X.on((i + 1) % 4, i) for i in range(4)])

    circ += XX('p4').on([0, 1])
    circ += YY('p5').on([1, 2])
    circ += ZZ('p6').on([2, 3])
    circ += BARRIER
    circ += UN(S, [0, 1]) + UN(T, [2, 3])
    circ += PhaseShift('p7').on(1, 0)
    circ += PhaseShift('p8').on(2, 3)
    circ += SWAP.on([0, 3])
    circ += RX('p9').on(0, 1)
    circ += RX('p10').on(3, 2)
    return circ


def random_circuit_extend():
    u = UnivMathGate('U', np.eye(16))
    circ = Circuit()
    circ += u.on([0, 1, 2, 3])
    circ += u.on([1, 2, 3, 4])
    circ += u.on([2, 3, 4, 5])
    return circ


def mq_random_circuit_pqc(n_qubit):
    template = random_circuit_template()
    circ = Circuit()
    for i in range(n_qubit - 3):
        circ += shift(add_prefix(template, f'l{i}'), i)
    return circ


def mq_random_circuit(n_qubit):
    circ = mq_random_circuit_pqc(n_qubit)
    np.random.seed(SEED)
    pr = np.random.uniform(-1, 1, len(circ.params_name))
    pr = dict(zip(circ.params_name, pr))
    return circ.apply_value(pr)


if __name__ == "__main__":
    from mindquantum import Simulator, Hamiltonian, QubitOperator
    pqc = mq_random_circuit_pqc(10)
    sim = Simulator('mqvector', pqc.n_qubits)
    ham = Hamiltonian(QubitOperator('Y1'))
    grad_ops = sim.get_expectation_with_grad(ham, pqc)
    x0 = np.random.uniform(-1, 1, len(pqc.params_name))
    grad_ops(x0)
    circ = mq_random_circuit(10)
    sim = Simulator('mqvector', 10)
    sim.apply_circuit(circ)
    # ham = Hamiltonian(QubitOperator('Z0'))
    # sim = Simulator('mqvector',1)
    # grad_ops=sim.get_expectation_with_grad(ham, Circuit().rx('a', 0))