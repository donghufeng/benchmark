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
from benchmark.task_preparation import generate_random_ham


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
    ham_text = generate_random_ham(n_qubits)
    ham = []
    for term in ham_text:
        ham.append([])
        for p, i in term:
            ham[-1].append((getattr(tc.gates, p.lower())(), [i]))
    # expectation = tc.backend.jit(circ.expectation)  # too long
    # expectation()  # warm up
    def run():
        e0 = 0
        for term in ham:
            # e0 += expectation(*term)
            e0 += circ.expectation(*term)
        return e0

    return run


if __name__ == "__main__":
    run = tc_random_ham_prepare("tensorflow", "cpu", 4)
    print(run())
