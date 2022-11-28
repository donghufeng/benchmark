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
from benchmark import TaskManage

tasks = TaskManage()
tasks.add_task("./intel/benchmark_random_circuit.py").add_arg("p", ["cpu"]).add_arg(
    "q", range(4, 24)
)
tasks.add_task("./intel/benchmark_random_ham.py").add_arg("p", ["cpu"]).add_arg(
    "q", range(4, 24)
)

tasks.add_task("./mindquantum/benchmark_random_circuit.py").add_arg(
    "p", ["cpu", "gpu"]
).add_arg("q", range(4, 24))
tasks.add_task("./mindquantum/benchmark_random_ham.py").add_arg(
    "p", ["cpu", "gpu"]
).add_arg("q", range(4, 24))
tasks.add_task("./mindquantum/benchmark_2_regular_qaoa.py").add_arg(
    "p", ["cpu", "gpu"]
).add_arg("q", range(4, 24))

tasks.add_task("./paddlequantum/benchmark_random_circuit.py").add_arg(
    "p", ["cpu", "gpu"]
).add_arg("q", range(4, 20))
tasks.add_task("./paddlequantum/benchmark_random_ham.py").add_arg(
    "p", ["cpu", "gpu"]
).add_arg("q", range(4, 20))
tasks.add_task("./paddlequantum/benchmark_2_regular_qaoa.py").add_arg(
    "p", ["cpu", "gpu"]
).add_arg("q", range(4, 20))

tasks.add_task("./quest/benchmark_random_circuit.py").add_arg(
    "p", ["cpu", "gpu"]
).add_arg("q", range(4, 24))
tasks.add_task("./quest/benchmark_random_ham.py").add_arg("p", ["cpu", "gpu"]).add_arg(
    "q", range(4, 24)
)

tasks.add_task("./qulacs/benchmark_random_circuit.py").add_arg(
    "p", ["cpu", "gpu"]
).add_arg("q", range(4, 24))
tasks.add_task("./qulacs/benchmark_random_ham.py").add_arg("p", ["cpu", "gpu"]).add_arg(
    "q", range(4, 24)
)
tasks.add_task("./qulacs/benchmark_2_regular_qaoa.py").add_arg(
    "p", ["cpu", "gpu"]
).add_arg("q", range(4, 24))

tasks.add_task("./tensorcircuit/benchmark_random_circuit.py").add_arg(
    "p", ["cpu", "gpu"]
).add_arg("q", range(4, 22))
tasks.add_task("./tensorcircuit/benchmark_random_ham.py").add_arg(
    "p", ["cpu", "gpu"]
).add_arg("q", range(4, 22))
tasks.add_task("./tensorcircuit/benchmark_2_regular_qaoa.py").add_arg(
    "p", ["cpu", "gpu"]
).add_arg("q", range(4, 22))

tasks.add_task("./tensorflowquantum/benchmark_random_circuit.py").add_arg(
    "p", ["cpu", "gpu"]
).add_arg("q", range(4, 24))
tasks.add_task("./tensorflowquantum/benchmark_random_ham.py").add_arg(
    "p", ["cpu", "gpu"]
).add_arg("q", range(4, 24))
tasks.add_task("./tensorflowquantum/benchmark_2_regular_qaoa.py").add_arg(
    "p", ["cpu", "gpu"]
).add_arg("q", range(4, 24))

tasks.generate_script()