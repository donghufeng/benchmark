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
from qulacs import ParametricQuantumCircuit, QuantumCircuit, gate
from qulacs import Observable
from mindquantum.core.circuit import Circuit
from mindquantum.core import gates as G
from mindquantum.core.operators import QubitOperator, count_qubits

def RaiseUnConvertible(g):
    raise ValueError(f"Cannot convert {g} for qulacs")

def mq_circ_to_qulacs(circ:Circuit):
    n_qubits = circ.n_qubits
    if circ.parameterized:
        out = ParametricQuantumCircuit(n_qubits)
    else:
        out = QuantumCircuit(n_qubits)
    for g in circ:
        if isinstance(g, (G.XGate, G.YGate, G.ZGate)):
            if not g.ctrl_qubits:
                getattr(out, f"add_{g.name}_gate")(g.obj_qubits[0])
            elif len(g.ctrl_qubits)>2:
                RaiseUnConvertible(g)
            else:
                if isinstance(g, G.XGate):
                    out.add_CNOT_gate(g.ctrl_qubits[0], g.obj_qubits[0])
                elif isinstance(g, G.ZGate):
                    out.add_CZ_gate(g.ctrl_qubits[0], g.obj_qubits[0])
                else:
                    RaiseUnConvertible(g)
        elif isinstance(g, G.HGate):
            if not g.ctrl_qubits:
                out.add_H_gate(g.obj_qubits[0])
            else:
                RaiseUnConvertible(g)
        elif isinstance(g,(G.RX, G.RY, G.RZ)):
            if g.parameterized:
                if not g.ctrl_qubits:
                    getattr(out, f"add_parametric_{g.name.upper()}_gate")(g.obj_qubits[0], 0.0)
                else:
                    RaiseUnConvertible(g)
            else:
                if not g.ctrl_qubits:
                    getattr(out, f"add_{g.name.upper()}_gate")(g.obj_qubits[0], g.coeff.const)
                else:
                    RaiseUnConvertible(g)
        elif isinstance(g, G.PhaseShift):
            if g.parameterized:
                RaiseUnConvertible(g)
            if not g.ctrl_qubits:
                out.add_U1_gate(g.obj_qubits[0], g.coeff.const)
            else:
                if len(g.ctrl_qubits)!=1:
                    RaiseUnConvertible(g)
                qulacs_u1 = gate.U1(g.obj_qubits[0], g.coeff.const)
                qulacs_u1.add_control_qubit(g.ctrl_qubits[0], 1)
                out.add_gate(qulacs_u1)
        elif isinstance(g, G.SWAPGate):
            if g.ctrl_qubits:
                RaiseUnConvertible(g)
            out.add_SWAP_gate(*g.obj_qubits)
        elif isinstance(g, (G.Rzz, G.Rxx, G.Ryy)):
            pauli_id = {'Rzz':3,'Rxx':1,'Ryy':2}[g.name]
            if g.ctrl_qubits:
                RaiseUnConvertible(g)
            if g.parameterized:
                out.add_parametric_multi_Pauli_rotation_gate(g.obj_qubits, [pauli_id, pauli_id], 0.0)
            else:
                out.add_multi_Pauli_rotation_gate(g.obj_qubits,[pauli_id, pauli_id], g.coeff.const)
        elif isinstance(g, G.BarrierGate):
            pass
        else:
            RaiseUnConvertible(g)
    return out

def mq_qubit_ops_to_qulacs(ops:QubitOperator, n_qubits=None):
    if n_qubits is None:
        n_qubits = count_qubits(ops)
    qulacs_ops = Observable(n_qubits)
    for term, coeff in ops.terms.items():
        if not coeff.is_const:
            raise ValueError(f"Cannot convert parameterized hamiltonian to qulacs.")
        qulacs_ops.add_operator(coeff.const, ' '.join(f"{str(word)} {idx}" for idx, word in term))
    return qulacs_ops
