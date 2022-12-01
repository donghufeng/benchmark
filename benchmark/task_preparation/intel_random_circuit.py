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

from benchmark.task_preparation import generate_random_circuit

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


def generate_intel_circuit(psi, n_qubits: int):
    out = []
    circ_text = generate_random_circuit(n_qubits)
    for gate_args in circ_text:
        gate = gate_args[0]
        if gate in ["x", "y", "z"]:
            out.append([getattr(psi, f"ApplyPauli{gate.upper()}"), (gate_args[1],)])
        elif gate == "h":
            out.append([psi.ApplyHadamard, (gate_args[1],)])
        elif gate == "s":
            out.append([lambda poi: apply_s(psi, poi), (gate_args[1],)])
        elif gate == "t":
            out.append([psi.ApplyT, (gate_args[1],)])
        elif gate in ["cx", "cy", "cz"]:
            out.append(
                [
                    getattr(psi, f"ApplyCPauli{gate[-1].upper()}"),
                    (gate_args[1], gate_args[2]),
                ]
            )
        elif gate in ["rx", "ry", "rz"]:
            out.append(
                [
                    getattr(psi, f"ApplyRotation{gate[-1].upper()}"),
                    (gate_args[1], gate_args[2]),
                ]
            )
        elif gate == "xx":
            out.append(
                [
                    lambda q1, q2, p: apply_xx(psi, q1, q2, p),
                    (gate_args[1], gate_args[2], gate_args[3]),
                ]
            )
        elif gate == "yy":
            out.append(
                [
                    lambda q1, q2, p: apply_yy(psi, q1, q2, p),
                    (gate_args[1], gate_args[2], gate_args[3]),
                ]
            )
        elif gate == "zz":
            out.append(
                [
                    lambda q1, q2, p: apply_zz(psi, q1, q2, p),
                    (gate_args[1], gate_args[2], gate_args[3]),
                ]
            )
        else:
            raise RuntimeError()
    return out


def intel_random_circuit_prepare(n_qubits: int):
    psi = simulator.QubitRegister(n_qubits, "base", 0, 0)
    circ = generate_intel_circuit(psi, n_qubits)

    def run():
        for i in circ:
            i[0](*i[1])
        return psi

    return run


if __name__ == "__main__":
    import numpy as np

    n_qubits = 10
    run = intel_random_circuit_prepare(n_qubits)
