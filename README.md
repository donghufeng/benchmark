# Benchmark

## Frameworks

|框架名称|公司|版本号|CPU|GPU|变分|Python API|
|-|-|-|-|-|-|-|
|MindQuantum|华为|0.8.0|✅|✅|✅|✅|
|qiskit|IBM|0.38.0|✅|✅|✅|✅|
|intel_qs|Intel|2.0.0-beta|✅|❌|❌|❌|
|paddle quantum|Baidu|2.2.1|✅|✅|✅|✅|
|tensorflow quantum|Google|0.7.2|✅|✅|✅|✅|
|qulacs|Qulacs|0.5.2|✅|✅|✅|✅|
|quest|QuEST|3.5.0|✅|✅|✅|❌|
|tensorcircuit|Tencent|0.5.0|✅|✅|✅|✅|

## Benchmark task

|任务名称|描述|比特范围|哈密顿量项数|量子门个数|OMP|
|-|-|-|-|-|-|
|random_circuit_qs|随机量子线路振幅模拟|4-24|/|1000-100|1-8|
|random_circuit_gradient|随机参数化量子线路梯度计算|4-24|1, Z0|1000-10|1-8|
|apply_random_hamiltonian|作用随机哈密顿量|4-24|1000-100|/|1-8|
|maxcut_SK_model_with_qaoa|利用qaoa解决全连接图的maxcut问题|4-24|/|/|1-8|
|vqe|分子基态能力求解|H2(4), LiH(12), BeH2(14), CH4(18)|/|/|1-8|
