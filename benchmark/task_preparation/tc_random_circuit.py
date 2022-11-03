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

import tensorcircuit as tc


def tc_random_circuit_pqc(n_qubit):

    def c_fun(params):
        circ = tc.Circuit(n_qubit)
        for i in range(n_qubit - 3):
            circ.h(i)
            circ.h(i + 1)
            circ.h(i + 2)
            circ.h(i + 3)
            circ.rx(i, theta=params[i * 11])
            circ.rx(i + 1, theta=params[i * 11 + 1])
            circ.rx(i + 2, theta=params[i * 11 + 2])
            circ.rx(i + 3, theta=params[i * 11 + 3])
            circ.cx(i, i + 1)
            circ.cx(i + 1, i + 2)
            circ.cx(i + 2, i + 3)
            circ.cx(i + 3, i)
            circ.rxx(i, i + 1, theta=params[i * 11 + 4])
            circ.ryy(i + 1, i + 2, theta=params[i * 11 + 5])
            circ.rzz(i + 2, i + 3, theta=params[i * 11 + 6])
            circ.s(i)
            circ.s(i + 1)
            circ.t(i + 2)
            circ.t(i + 3)
            circ.cphase(i, i + 1, theta=params[i * 11 + 7])
            circ.cphase(i + 3, i + 2, theta=params[i * 11 + 8])
            circ.swap(i, i + 3)
            circ.crx(i + 1, i, theta=params[i * 11 + 9])
            circ.crx(i + 2, i + 3, theta=params[i * 11 + 10])
        return circ

    return c_fun


if __name__ == '__main__':
    import numpy as np
    tc.set_backend('tensorflow')
    tc.set_dtype('complex128')

    x = tc.backend.cast(np.random.uniform(-1, 1, 2 * 11), "float64")
    c_fun = tc_random_circuit_pqc(5)
    wave_fun = tc.backend.jit(lambda x: c_fun(x).wavefunction())
    wave_fun(x)
    def energy(x):
        circ = c_fun(x)
        e0 = circ.expectation((tc.gates.y(), [1]))
        return tc.backend.real(e0)

    g = tc.backend.value_and_grad(energy)
    g = tc.backend.jit(g)
    g(x)
