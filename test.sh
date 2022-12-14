
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



python3 task1.py -q 5 -p cpu -n $file_name
python3 task1.py -q 5 -p gpu -n $file_name
python3 task1.py -q 6 -p cpu -n $file_name
python3 task1.py -q 6 -p gpu -n $file_name
