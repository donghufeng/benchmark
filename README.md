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

## Benchmark task

量子线路或者哈密顿量由框架自己生成，不由其他框架转化。

|任务名称|描述|比特范围|哈密顿量项数|量子门个数|OMP|Layer|
|-|-|-|-|-|-|-|
|random_circuit_qs|随机量子线路振幅模拟|4-24|/|25*n|1-8|/|
|random_hamiltonian_expectation|随机哈密顿量期望值|4-24|$\min(1000-100, n_\text{qubit}^4)$|/|1-8|/|
|maxcut_random_2_regular_with_qaoa|利用qaoa解决随机2-regular的maxcut问题|4-24|/|/|1-8|1|

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
