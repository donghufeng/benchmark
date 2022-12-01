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
"""quest random circuit"""
from benchmark.task_preparation import generate_random_circuit


def quest_random_circuit_prepare(platform: str, n_qubits: int):
    if platform == "cpu":
        import quest_test
    elif platform == "gpu":
        import quest_test_gpu as quest_test
    else:
        raise RuntimeError(f"platform {platform} not supported for quest.")
    test = quest_test.random_circuit_test(n_qubits)
    circ_text = generate_random_circuit(n_qubits)

    def run():
        for g in circ_text:
            test.apply_gate(*g)
        return test

    return run


if __name__ == "__main__":
    run = quest_random_circuit_prepare("cpu", 5)
    run()
