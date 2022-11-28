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
"""Benchmark tensorflow quantum for 2 regular max cut."""
import cirq
import networkx as nx
import numpy as np
import sympy

from benchmark import SEED

# import tensorflow as tf
# import tensorflow_quantum as tfq
# from tensorflow_quantum.core.ops import tfq_adj_grad_op
# from tensorflow_quantum.python import util


def tf_qaoa_prepare(platform: str, n_qubit: int):
    import os

    if platform == "gpu":
        import tensorflow as tf

        gpu = tf.config.list_physical_devices("GPU")
        tf.config.experimental.set_memory_growth(device=gpu[0], enable=True)
    elif platform == "cpu":
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
        import tensorflow as tf
    else:
        raise RuntimeError(
            f"Platform {platform} for tf_random_ham_prepare unrecognized, should be cpu or gpu."
        )
    import tensorflow_quantum as tfq
    from tensorflow_quantum.python import util

    net = nx.random_regular_graph(2, n_qubit, SEED)
    edges = list(net.edges)
    circuit = cirq.Circuit()
    qubits = [cirq.GridQubit(0, i) for i in range(n_qubit)]
    params = []
    for q in qubits:
        circuit.append(cirq.H(q))
    for i, j in edges:
        p = sympy.symbols(f"p{len(params)}")
        params.append(p)
        circuit.append(cirq.ZZ(qubits[i], qubits[j]) ** p)
    for q in qubits:
        p = sympy.symbols(f"p{len(params)}")
        params.append(p)
        circuit.append(cirq.X(q) ** p)
    ham = sum(cirq.Z(qubits[i]) * cirq.Z(qubits[j]) for i, j in edges)
    circuit = util.convert_to_tensor([circuit])
    ham = tfq.convert_to_tensor([[ham]])
    symbol_values = np.array([np.random.normal(size=[len(params)])], dtype=np.float32)
    symbol_values_t = tf.Variable(tf.convert_to_tensor(symbol_values))
    symbol_names = tf.convert_to_tensor([str(i) for i in params])
    my_op = tfq.get_expectation_op()
    adjoint_differentiator = tfq.differentiators.Adjoint()
    op = adjoint_differentiator.generate_differentiable_op(analytic_op=my_op)

    @tf.function
    def f():
        with tf.GradientTape() as g:
            g.watch(symbol_values_t)
            expectations = op(circuit, symbol_names, symbol_values_t, ham)
        grads = g.gradient(expectations, [symbol_values_t])
        return grads, expectations

    return f


if __name__ == "__main__":
    tf_grad_ops = tf_qaoa_prepare("cpu", 5)
    f, g = tf_grad_ops()
