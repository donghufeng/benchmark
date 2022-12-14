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
# from benchmark import TaskManage

# tasks = TaskManage()
# tasks.add_task("./intel/benchmark_random_circuit.py").add_arg("p",
#                                                               ["cpu"]).add_arg(
#                                                                   "q",
#                                                                   range(4, 24))
# tasks.add_task("./intel/benchmark_random_ham.py").add_arg(
#     "p", ["cpu"]).add_arg("q", range(4, 24))

# tasks.add_task("./mindquantum/benchmark_random_circuit.py").add_arg(
#     "p", ["cpu", "gpu"]).add_arg("q", range(4, 24))
# tasks.add_task("./mindquantum/benchmark_random_ham.py").add_arg(
#     "p", ["cpu", "gpu"]).add_arg("q", range(4, 24))
# tasks.add_task("./mindquantum/benchmark_4_regular_qaoa.py").add_arg(
#     "p", ["cpu", "gpu"]).add_arg("q", range(5, 24))

# tasks.add_task("./paddlequantum/benchmark_random_circuit.py").add_arg(
#     "p", ["cpu", "gpu"]).add_arg("q", range(4, 20))
# tasks.add_task("./paddlequantum/benchmark_random_ham.py").add_arg(
#     "p", ["cpu", "gpu"]).add_arg("q", range(4, 13))
# tasks.add_task("./paddlequantum/benchmark_4_regular_qaoa.py").add_arg(
#     "p", ["cpu"]).add_arg("q", range(5, 20))
# tasks.add_task("./paddlequantum/benchmark_4_regular_qaoa.py").add_arg(
#     "p", ["gpu"]).add_arg("q", range(5, 23))

# tasks.add_task("./quest/benchmark_random_circuit.py").add_arg(
#     "p", ["cpu", "gpu"]).add_arg("q", range(4, 24))
# tasks.add_task("./quest/benchmark_random_ham.py").add_arg(
#     "p", ["cpu", "gpu"]).add_arg("q", range(4, 24))

# tasks.add_task("./qulacs/benchmark_random_circuit.py").add_arg(
#     "p", ["cpu", "gpu"]).add_arg("q", range(4, 24))
# tasks.add_task("./qulacs/benchmark_random_ham.py").add_arg(
#     "p", ["cpu", "gpu"]).add_arg("q", range(4, 24))
# tasks.add_task("./qulacs/benchmark_4_regular_qaoa.py").add_arg(
#     "p", ["cpu"]).add_arg("q", range(5, 24))

# # tasks.add_task("./tensorcircuit/benchmark_random_circuit.py").add_arg(
# #     "p", ["cpu", "gpu"]
# # ).add_arg("q", range(4, 17))
# # tasks.add_task("./tensorcircuit/benchmark_random_ham.py").add_arg(
# #     "p", ["cpu", "gpu"]
# # ).add_arg("q", range(4, 17))
# # tasks.add_task("./tensorcircuit/benchmark_4_regular_qaoa.py").add_arg(
# #     "p", ["cpu", "gpu"]
# # ).add_arg("q", range(5, 17))

# tasks.add_task("./tensorflowquantum/benchmark_random_circuit.py").add_arg(
#     "p", ["cpu", "gpu"]).add_arg("q", range(4, 24))
# tasks.add_task("./tensorflowquantum/benchmark_random_ham.py").add_arg(
#     "p", ["cpu", "gpu"]).add_arg("q", range(4, 24))
# tasks.add_task("./tensorflowquantum/benchmark_4_regular_qaoa.py").add_arg(
#     "p", ["cpu", "gpu"]).add_arg("q", range(5, 24))

# tasks.add_task("./qiskit/benchmark_random_circuit.py").add_arg(
#     "p", ["cpu", "gpu"]).add_arg("q", range(4, 24))
# tasks.add_task("./qiskit/benchmark_random_ham.py").add_arg(
#     "p", ["cpu", "gpu"]).add_arg("q", range(4, 24))

# tasks.add_task("./qpanda/benchmark_random_circuit.py").add_arg(
#     "p", ["cpu", "gpu"]).add_arg("q", range(4, 20))
# tasks.add_task("./qpanda/benchmark_random_ham.py").add_arg(
#     "p", ["cpu", "gpu"]).add_arg("q", range(4, 20))

# tasks.generate_script()

import toml
from benchmark import TaskManage
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-c",
                    "--config",
                    help="toml style config file path",
                    type=str,
                    default="benchmark.toml")
args = parser.parse_args()

tasks_conf = toml.load(args.config)

all_framework = tasks_conf['benchmark-framework']['frameworks']

tasks = TaskManage()

for fw in all_framework:
    fw_tasks = tasks_conf['framework'][fw]
    for task, arg in fw_tasks.items():
        this_task = tasks.add_task(f"./{fw}/{task}.py")
        this_task.add_arg("p", arg['platform'])
        if 'gate' in arg:
            this_task.add_arg('g', arg['gate'])
        this_task.add_arg('q', range(arg['qubit_min'], arg['qubit_max']))
tasks.generate_script()
