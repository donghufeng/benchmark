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

|任务名称|描述|比特范围|
|-|-|-|
|random_circuit_qs|随机量子线路振幅模拟|4-24|
|random_circuit_gradient|随机参数化量子线路梯度计算|4-24|
|apply_random_hamiltonian|作用随机哈密顿量|4-24|
|maxcut_SK_model_with_qaoa|利用qaoa解决全连接图的maxcut问题|4-24, $n_\text{layer}=\text{Int}(1-(n_\text{qubit}-24)*19/20)$|
|vqe|分子基态能力求解|H2(4), LiH(12), BeH2(14), CH4(18)|
