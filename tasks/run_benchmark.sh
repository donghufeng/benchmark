
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



python3 ./mindquantum/benchmark_random_circuit_opt.py --p cpu --q 4 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p cpu --q 5 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p cpu --q 6 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p cpu --q 7 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p cpu --q 8 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p cpu --q 9 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p cpu --q 10 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p cpu --q 11 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p cpu --q 12 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p cpu --q 13 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p cpu --q 14 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p cpu --q 15 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p cpu --q 16 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p cpu --q 17 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p cpu --q 18 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p cpu --q 19 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p cpu --q 20 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p cpu --q 21 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p cpu --q 22 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p cpu --q 23 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p gpu --q 4 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p gpu --q 5 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p gpu --q 6 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p gpu --q 7 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p gpu --q 8 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p gpu --q 9 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p gpu --q 10 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p gpu --q 11 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p gpu --q 12 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p gpu --q 13 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p gpu --q 14 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p gpu --q 15 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p gpu --q 16 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p gpu --q 17 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p gpu --q 18 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p gpu --q 19 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p gpu --q 20 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p gpu --q 21 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p gpu --q 22 -n $file_name
python3 ./mindquantum/benchmark_random_circuit_opt.py --p gpu --q 23 -n $file_name
