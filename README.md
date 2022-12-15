# Benchmark

## Frameworks

|框架名称|公司|版本号|CPU|GPU|原生支持变分|Python API|jit|原生支持jw变换|Benchmark进度|
|-|-|-|-|-|-|-|-|-|-|
|MindQuantum|华为|0.8.0|✅|✅|✅|✅|✅|✅|✅|
|qiskit|IBM|0.38.0|✅|✅|❌|✅|❌|❌||
|intel_qs|Intel|2.0.0-beta|✅|❌|❌|❌|❌|❌|✅|
|paddle quantum|Baidu|2.2.1|✅|✅|❌|✅|✅|❌|✅|
|tensorflow quantum|Google|0.7.2|✅|✅|✅|✅|✅|❌|✅|
|qulacs|Qulacs|0.5.2|✅|✅|✅|✅|❌|❌|✅|
|quest|Oxford|3.5.0|✅|✅|✅|❌|❌|❌|✅|
|tensorcircuit|Tencent|0.5.0|✅|✅|❌|✅|✅|❌|✅|
|pyqpanda|本源|3.7.15|✅|✅|✅|✅|❌|✅|✅|

## Benchmark task

量子线路或者哈密顿量由框架自己生成，不由其他框架转化。

|任务名称|描述|比特范围|哈密顿量项数|量子门个数|OMP|Layer|
|-|-|-|-|-|-|-|
|random_circuit_qs|随机量子线路振幅模拟|4-24|/|25*n|1-8|/|
|random_hamiltonian_expectation|随机哈密顿量期望值|4-24|$\min(1000-100, n_\text{qubit}^4)$|/|1-8|/|
|maxcut_random_4_regular_with_qaoa|利用qaoa解决随机4-regular的maxcut问题|4-24|/|/|1-8|1|

## Task Detail

### random_circuit_qs

量子门可选集合：

```text
x, y, z, h, s, t, cx, cy, cz, rx, ry, rz, xx, yy, zz
```

总量子门个数公式：

$$N = 40(4-n) + 1000$$

统一随机数种子。

### random_hamiltonian_expectation

可选 Qubit 算符：

```text
X, Y, Z
```

总算符数公式：

$$N = 48(4-n) + 1000$$

统一随机数种子。

### maxcut_random_2_regular_with_qaoa

随机的2-regular图，seed=42。


### jw_transform

随机费米子算符的jw变换，4比特模板:

```text
-----a-------adg------------a-------
-----adg--------------a-----a-------
-----a-------adg------------adg-----
-----adg--------------a-----adg-----
```

## task format

```text
def {framework_name}_{task_name}_prepare(*prep_args, **prep_kwargs): -> run_task_method
```

## Conclution

### Qulacs

Parameter shift (relative slow) and adjoint gradient (relative fast).
Only support rx, ry, rz, rot_pauli, only **CPU**.

### TensorFlow Quantum

Only support float type.

## How to use

### Prepare environment

The environment is prepared based on what you want to benchmark. For example, the default benchmark task configuration is in `./tasks/benchmark.toml`, you can prepare the environment by:

```bash
bash prepare_venv.sh ./tasks/benchmark.toml
```
This script can install frameworks you want to benchmark.

> If you want to add new framework to this benchmark project, you need to implement a installing script in `env_scripts` and add it to `env_scripts/install_benchmark_lib.sh`.

### Activate environment

If you successfully prepared the environment, then you can run following code to activate it.

```bash
. prepare_venv.sh ./tasks/benchmark.toml
```

Your virtual python environment should be activated. At this this time, feel free to commit out some frameworks or benchmark tasks in configuration file.

### Explain

How this benchmark framework works?

Basically, we run different python scripts to do benchmark, for example if you want to benchmark a task in different qubit `q` and different platform, you can do like:

```bash
python task1.py -q 5 -p cpu
python task1.py -q 6 -p cpu
python task2.py -q 5 -p gpu
python task2.py -q 6 -p gpu
```

The rest things is to how to organize tasks, how to implement the task and how to show benchmark result. We will explain one by one.

### How to organize tasks

This framework support a `TaskManage` for manage different tasks.

```python
from benchmark import TaskManage
tasks = TaskManage()
```

Add a script as a task:

```python
task = tasks.add_task('task1.py')
```

Add arguments to this task:

```python
task.add_arg('q', [5, 6])
task.add_arg('p', ['cpu', 'gpu'])
```

Generate task file:

```python
tasks.generate_script(script_name="test.sh", cmd='python3')
```

And you will get a `test.sh`, let's see what it is.

```bash
python3 task1.py -q 5 -p cpu -n $file_name
python3 task1.py -q 5 -p gpu -n $file_name
python3 task1.py -q 6 -p cpu -n $file_name
python3 task1.py -q 6 -p gpu -n $file_name
```

`file_name` is a argument you need to send to `test.sh`. Now you can run the benchmark script like:

```bash
bash test.sh result
```

### How to implement task file

Basically, this framework benchmark performance by running a method several times to measure the time consuming. We have a `Benchmark` object to implement benchmark. Suppose we want to benchmark the following method:

```python
import argparse
from mindquantum import *

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--platform", help="platform", type=str, default="cpu")
parser.add_argument("-q", "--qubit", help="number of qubit", type=int, default=4)
args = parser.parse_args()

def tasks(platform, n_qubit):
    sim = Simulator(platform, n_qubit)
    circ =  qft(n_qubit)
    def run(layer):
        for l in range(layer):
            sim.apply_circuit(circ)
        return sim
    return run

run = tasks(args.platform, args.qubit)
```

We can setup the benchmark by:

```python
from benchmark import Benchmark
Benchmark(file_name='xxx.json',
          file_path='./',
          task_name='qft',
          task_params={'platform': args.platform, 'n_qubit': args.qubit},
          task_fun=run,
          task_args=(4, ),
          warmup=True
          )
```

The `file_name` and `file_path` is where you will save your benchmark result. `task_name` is how to identify your benchmark in the result. `task_params` is how your benchmark setup, and it can also help to identify which run you are in a same task. `task_fun` is just the method you want to benchmark. `task_args` is the runtime arguments for `task_fun`. `warmup` is set to run several times before we measure the time consuming.

> Once the benchmark setup, the benchmark will run automatically.
