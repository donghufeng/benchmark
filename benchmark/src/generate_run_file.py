# Copyright 2022 Huawei Technologies Co., Ltd
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
"""Generate run script."""
import itertools
from typing import List

meta = """
#!/bin/bash
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

if [ $# -eq 0 ]; then
    echo 'please enter file name: '
    read file_name
else
    file_name=$1
fi

echo "Benchmark file is ${file_name}.json"


"""

# task1 = {
#     'filename': 'test_qnn.py',
#     's': ['mqcpu', 'mqgpu', 'projectq'],
#     'q': range(4, 8)
# }

# task2 = {
#     'filename': 'test_apply_hamiltonian.py',
#     's': ['mqcpu', 'mqgpu', 'projectq'],
#     'q': range(4, 8)
# }

# task3 = {
#     'filename': 'test_benchmark_random_circuit.py',
#     's': ['mqcpu', 'mqgpu', 'projectq'],
#     'q': range(4, 8)
# }

# def gene_cmd(task):
#     filename = task['filename']
#     args = {k: v for k, v in task.items() if k != 'filename'}
#     all_args = list(itertools.product(*args.values()))
#     out = []
#     for arg in all_args:
#         tmp = ' '.join(
#             [f"-{i} {j}" for i, j in dict(zip(args.keys(), arg)).items()])
#         out.append(f"python {filename} {tmp} -n $file_name")
#     return out

# with open('run_benchmark.sh', 'w') as f:
#     f.writelines(meta)
#     f.writelines('\n'.join(gene_cmd(task1)) + '\n')
#     f.writelines('\n'.join(gene_cmd(task2)) + '\n')
#     f.writelines('\n'.join(gene_cmd(task3)) + '\n')


class Task:

    def __init__(self, task_file: str):
        self.task_file = task_file
        self.args = {}

    def add_arg(self, arg_name, arg_values) -> "Task":
        self.args[arg_name] = arg_values
        return self

    def generate_cmd(self, cmd="python3"):
        all_args = list(itertools.product(*self.args.values()))
        out = []
        for arg in all_args:
            tmp = " ".join([
                f"-{i} {j}"
                for i, j in dict(zip(self.args.keys(), arg)).items()
            ])
            out.append(f"{cmd} {self.task_file} {tmp} -n $file_name")
        return out


class TaskManage:

    def __init__(self):
        self.tasks: List[Task]
        self.tasks = []

    def add_task(self, task_file) -> Task:
        task = Task(task_file)
        self.tasks.append(task)
        return task

    def generate_script(self, scripe_name="run_benchmark.sh", cmd='python3'):
        with open(scripe_name, "w") as f:
            f.writelines(meta)
            for task in self.tasks:
                f.writelines("\n" + "\n".join(task.generate_cmd(cmd)) + "\n")


if __name__ == "__main__":
    simulators = ["mqcpu", "mqgpu", "projectq"]
    n_qubits = range(4, 22)
    tasks = TaskManage()
    tasks.add_task("test_apply_hamiltonian.py").add_arg("q", n_qubits).add_arg(
        "s", simulators)

    tasks.add_task("test_qnn.py").add_arg("q",
                                          n_qubits).add_arg("s", simulators)

    tasks.add_task("test_benchmark_random_circuit.py").add_arg(
        "q", n_qubits).add_arg("s", simulators)
    tasks.add_task("test_qaoa.py").add_arg("q",
                                           n_qubits).add_arg("s", simulators)
    tasks.generate_script()
