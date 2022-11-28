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


def tc_random_ham(circ: "tc.Circuit", n_qubit: int):
    import tensorcircuit.gates as tg

    e0 = 0.0
    for i in range(n_qubit - 3):
        e0 += circ.expectation(
            (tg.y(), [i]), (tg.y(), [i + 1]), (tg.y(), [i + 2]), (tg.y(), [i + 3])
        )
        e0 += circ.expectation((tg.x(), [i]), (tg.x(), [i + 2]))
        e0 += circ.expectation((tg.z(), [i + 1]), (tg.z(), [i + 3]))
        e0 += circ.expectation(
            (tg.z(), [i]), (tg.y(), [i + 1]), (tg.x(), [i + 2]), (tg.z(), [i + 3])
        )

    return e0


def tc_random_ham_prepare(backend: str, platform: str, n_qubits: int):
    import os

    if platform == "gpu":
        import tensorflow as tf

        gpu = tf.config.list_physical_devices("GPU")
        tf.config.experimental.set_memory_growth(device=gpu[0], enable=True)
    elif platform == "cpu":
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    else:
        raise RuntimeError(
            f"Platform {platform} for tf_random_circuit_prepare unrecognized, should be cpu or gpu."
        )

    import tensorcircuit as tc

    tc.set_backend(backend)
    tc.set_dtype("complex128")
    if backend != "tensorflow":
        raise RuntimeError("We only benchmark for tensorflow backend.")
    circ = tc.Circuit(n_qubits)
    for i in range(n_qubits):
        circ.h(i)

    def run():
        return tc_random_ham(circ, n_qubits)

    return run


if __name__ == "__main__":
    import tensorcircuit as tc

    n_qubit = 5
    circ = tc.Circuit(n_qubit)
    for i in range(n_qubit):
        circ.h(i)
    e0 = tc_random_ham(circ, n_qubit)
    print(e0)
