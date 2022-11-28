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
"""Benchmark random circuit for intel."""

import intelqs_py as simulator
import numpy as np

pi_2 = np.pi / 2


def apply_zz(psi, i, j, p):
    psi.ApplyCPauliX(i, j)
    psi.ApplyRotationZ(j, 2 * p)
    psi.ApplyCPauliX(i, j)


def apply_xx(psi, i, j, p):
    psi.ApplyHadamard(i)
    psi.ApplyHadamard(j)
    psi.ApplyCPauliX(i, j)
    psi.ApplyRotationZ(j, 2 * p)
    psi.ApplyCPauliX(i, j)
    psi.ApplyHadamard(j)
    psi.ApplyHadamard(i)


def apply_yy(psi, i, j, p):
    psi.ApplyRotationX(i, pi_2)
    psi.ApplyRotationX(j, pi_2)
    psi.ApplyCPauliX(i, j)
    psi.ApplyRotationZ(j, 2 * p)
    psi.ApplyCPauliX(i, j)
    psi.ApplyRotationX(j, pi_2)
    psi.ApplyRotationX(i, pi_2)


def apply_s(psi, i):
    psi.ApplyT(i)
    psi.ApplyT(i)


def intel_random_circuit(n_qubits, params):
    psi = simulator.QubitRegister(n_qubits, "base", 0, 0)
    for i in range(n_qubits - 3):
        psi.ApplyHadamard(i)
        psi.ApplyHadamard(i + 1)
        psi.ApplyHadamard(i + 2)
        psi.ApplyHadamard(i + 3)
        psi.ApplyRotationX(i, params[i * 11])
        psi.ApplyRotationX(i + 1, params[i * 11 + 1])
        psi.ApplyRotationX(i + 2, params[i * 11 + 2])
        psi.ApplyRotationX(i + 3, params[i * 11 + 3])
        psi.ApplyCPauliX(i, i + 1)
        psi.ApplyCPauliX(i + 1, i + 2)
        psi.ApplyCPauliX(i + 2, i + 3)
        psi.ApplyCPauliX(i + 3, i)
        apply_xx(psi, i, i + 1, params[i * 11 + 4])
        apply_yy(psi, i + 1, i + 2, params[i * 11 + 5])
        apply_zz(psi, i + 2, i + 3, params[i * 11 + 6])
        apply_s(psi, i)
        apply_s(psi, i + 1)
        psi.ApplyT(i + 2)
        psi.ApplyT(i + 3)
        psi.ApplyCRotationZ(i, i + 1, params[i * 11 + 7])
        psi.ApplyCRotationZ(i + 3, i + 2, params[i * 11 + 8])
        psi.ApplySwap(i, i + 3)
        psi.ApplyCRotationX(i + 1, i, params[i * 11 + 9])
        psi.ApplyCRotationX(i + 2, i + 3, params[i * 11 + 10])
    return psi


def intel_random_circuit_prepare(n_qubits: int):
    p0 = np.random.uniform(-1, 1, (n_qubits - 3) * 11)

    def run():
        return intel_random_circuit(n_qubits, p0)

    return run


if __name__ == "__main__":
    import numpy as np

    n_qubits = 10
    p0 = np.random.uniform(-1, 1, (n_qubits - 3) * 11)
    intel_random_circuit(n_qubits, p0)
