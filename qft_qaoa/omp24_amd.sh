
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



export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_qft.py -p cpu -q 15 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_qft.py -p cpu -q 16 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_qft.py -p cpu -q 17 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_qft.py -p cpu -q 18 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_qft.py -p cpu -q 19 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_qft.py -p cpu -q 20 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_qft.py -p cpu -q 21 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_qft.py -p cpu -q 22 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_qft.py -p cpu -q 23 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_qft.py -p cpu -q 24 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_qft.py -p cpu -q 25 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_qft.py -p cpu -q 26 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_qft.py -p cpu -q 27 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_qft.py -p cpu -q 28 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_qft.py -p cpu -q 29 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_qft.py -p cpu -q 30 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_qft.py -p cpu -q 31 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_qft.py -p cpu -q 32 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_qft.py -p cpu -q 33 -n $file_name

export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_4_regular_qaoa.py -p cpu -q 15 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_4_regular_qaoa.py -p cpu -q 16 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_4_regular_qaoa.py -p cpu -q 17 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_4_regular_qaoa.py -p cpu -q 18 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_4_regular_qaoa.py -p cpu -q 19 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_4_regular_qaoa.py -p cpu -q 20 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_4_regular_qaoa.py -p cpu -q 21 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_4_regular_qaoa.py -p cpu -q 22 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_4_regular_qaoa.py -p cpu -q 23 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_4_regular_qaoa.py -p cpu -q 24 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_4_regular_qaoa.py -p cpu -q 25 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_4_regular_qaoa.py -p cpu -q 26 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_4_regular_qaoa.py -p cpu -q 27 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_4_regular_qaoa.py -p cpu -q 28 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_4_regular_qaoa.py -p cpu -q 29 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_4_regular_qaoa.py -p cpu -q 30 -n $file_name
export OMP_NUM_THREADS=24;python ./mindquantum/benchmark_4_regular_qaoa.py -p cpu -q 31 -n $file_name

export OMP_NUM_THREADS=24;python ./qulacs/benchmark_qft.py -p cpu -q 15 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_qft.py -p cpu -q 16 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_qft.py -p cpu -q 17 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_qft.py -p cpu -q 18 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_qft.py -p cpu -q 19 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_qft.py -p cpu -q 20 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_qft.py -p cpu -q 21 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_qft.py -p cpu -q 22 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_qft.py -p cpu -q 23 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_qft.py -p cpu -q 24 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_qft.py -p cpu -q 25 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_qft.py -p cpu -q 26 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_qft.py -p cpu -q 27 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_qft.py -p cpu -q 28 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_qft.py -p cpu -q 29 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_qft.py -p cpu -q 30 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_qft.py -p cpu -q 31 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_qft.py -p cpu -q 32 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_qft.py -p cpu -q 33 -n $file_name

export OMP_NUM_THREADS=24;python ./qulacs/benchmark_4_regular_qaoa.py -p cpu -q 15 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_4_regular_qaoa.py -p cpu -q 16 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_4_regular_qaoa.py -p cpu -q 17 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_4_regular_qaoa.py -p cpu -q 18 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_4_regular_qaoa.py -p cpu -q 19 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_4_regular_qaoa.py -p cpu -q 20 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_4_regular_qaoa.py -p cpu -q 21 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_4_regular_qaoa.py -p cpu -q 22 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_4_regular_qaoa.py -p cpu -q 23 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_4_regular_qaoa.py -p cpu -q 24 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_4_regular_qaoa.py -p cpu -q 25 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_4_regular_qaoa.py -p cpu -q 26 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_4_regular_qaoa.py -p cpu -q 27 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_4_regular_qaoa.py -p cpu -q 28 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_4_regular_qaoa.py -p cpu -q 29 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_4_regular_qaoa.py -p cpu -q 30 -n $file_name
export OMP_NUM_THREADS=24;python ./qulacs/benchmark_4_regular_qaoa.py -p cpu -q 31 -n $file_name
