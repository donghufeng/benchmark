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
import toml
from benchmark import TaskManage
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-c",
                    "--config",
                    help="toml style config file path",
                    type=str,
                    default="benchmark.toml")
parser.add_argument("-t",
                    "--threads",
                    help="thread number",
                    type=int,
                    default=655325)
parser.add_argument("-s",
                    "--script",
                    help="output run script",
                    type=str,
                    default="run_benchmark.sh")
args = parser.parse_args()

tasks_conf = toml.load(args.config)

all_framework = tasks_conf['benchmark-framework']['frameworks']

tasks = TaskManage()

# 1. add_task will add a python script to run.
# For example:
# >>> tasks.add_task("xxx.py")
# will generate a cmd like:
#    python xxx.py

# 2. add_arg will pass argument to python script
# For example:
# >>> task.add_arg("x", [a, b, c])
# will generate a cmd like:
#    python xxx.py -x a
#    python xxx.py -x b
#    python xxx.py -x c

# 3. generate_script will generate a file named `run_benchmark.sh`
# you can run it and store the  benchmark result to a file like:
#    bash run_benchmark.sh res
# After the benchmark finished, a file named `res.json` will be generated.

for fw in all_framework:
    fw_tasks = tasks_conf['framework'][fw]
    for task, arg in fw_tasks.items():
        this_task = tasks.add_task(f"./{fw}/{task}.py")
        this_task.add_arg("p", arg['platform'])
        this_task.add_arg('q', range(arg['qubit_min'], arg['qubit_max']))
script_name = args.script
if not script_name.endswith('.sh'):
    script_name += '.sh'
tasks.generate_script(script_name=script_name, cmd=f'export OMP_NUM_THREADS={args.threads};python')
