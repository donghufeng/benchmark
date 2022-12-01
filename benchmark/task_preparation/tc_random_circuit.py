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
import numpy as np

from benchmark.task_preparation import generate_random_circuit


def tc_random_circuit(n_qubit):
    import tensorcircuit as tc

    circ = tc.Circuit(n_qubit)
    circ_text = generate_random_circuit(n_qubit)
    for gate_args in circ_text:
        gate = gate_args[0]
        if gate in ["x", "y", "z", "h", "s", "t"]:
            getattr(circ, gate)(gate_args[1])
        elif gate in ["cx", "cy", "cz"]:
            getattr(circ, gate)(gate_args[1], gate_args[2])
        elif gate in ["rx", "ry", "rz"]:
            getattr(circ, gate)(gate_args[1], theta=gate_args[2])
        elif gate in ["xx", "yy", "zz"]:
            getattr(circ, f"r{gate}")(gate_args[1], gate_args[2], theta=gate_args[3])
        else:
            raise RuntimeError()
    return circ


def tc_random_circuit_prepare(backend: str, platform: str, n_qubits: int):
    import os

    if platform == "gpu":
        import tensorflow as tf

        gpu = tf.config.list_physical_devices("GPU")
        tf.config.experimental.set_memory_growth(device=gpu[0], enable=True)
    elif platform == "cpu":
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    else:
        raise RuntimeError(
            f"Platform {platform} for tc_random_circuit_prepare unrecognized, should be cpu or gpu."
        )

    import tensorcircuit as tc

    tc.set_backend(backend)
    tc.set_dtype("complex128")
    if backend != "tensorflow":
        raise RuntimeError("We only benchmark for tensorflow backend.")
    c_fun = tc_random_circuit(n_qubits)
    # wave_fun = tc.backend.jit(c_fun.wavefunction)  # too long

    def run():
        return c_fun.wavefunction()

    return run


if __name__ == "__main__":
    run = tc_random_circuit_prepare("tensorflow", "cpu", 4)
    run()
