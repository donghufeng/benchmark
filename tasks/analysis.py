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
"""Analysis data."""
import json
from typing import Union, List


def load_from_json(filename: str):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def find_all_task(data: dict):
    out = []
    for v in data.values():
        if "task_name" not in v:
            raise RuntimeError("Task not defined.")
        task_name = v["task_name"]
        if task_name not in out:
            out.append(task_name)
    return out


def find_all_keys(data: dict, params: str):
    out = []
    for v in data.values():
        if params in v.get('task_params'):
            value = v.get('task_params').get(params)
            if value not in out:
                out.append(value)
    return out


def filter_task(data: dict, task: str):
    out = {}
    for k, v in data.items():
        if v.get('task_name') == task:
            out[k] = v
    return out


def filter_task_params(data: dict, task_param_name: str, task_param_val):
    """Find all data that match task_params key and value with given value."""
    out = {}
    for k, v in data.items():
        if task_param_name in v.get('task_params') and v.get(
                'task_params').get(task_param_name) == task_param_val:
            out[k] = v
    return out


class DataFrame:

    def __init__(self, data: Union[dict, str]):
        if isinstance(data, str):
            self.data = load_from_json(data)
        elif isinstance(data, dict):
            self.data = data
        else:
            raise TypeError("data requires dict or str.")

    def find_all_task(self):
        return find_all_task(self.data)

    def split_by_tasks(self) -> List["DataFrame"]:
        return [self.filter_task(i) for i in self.find_all_task()]

    def find_all_params(self):
        out = []
        for v in self.data.values():
            for i in v.get('task_params'):
                if i not in out:
                    out.append(i)
        return out

    def find_all_keys(self, params: str):
        return find_all_keys(self.data, params)

    def filter_task(self, task_name: str):
        return DataFrame(filter_task(self.data, task_name))

    def filter_task_params(self, task_param_name: str,
                           task_param_val) -> "DataFrame":
        return DataFrame(
            filter_task_params(self.data, task_param_name, task_param_val))

    def split_by_params(self, task_param_name: str) -> List["DataFrame"]:
        return [
            self.filter_task_params(task_param_name, i)
            for i in self.find_all_keys(task_param_name)
        ]

    def assert_single_task(self):
        if len(self.find_all_task) != 1:
            raise ValueError("DataFrame has multiple tasks.")

    def assert_single_params(self, task_parm_name):
        if len(self.find_all_keys(task_parm_name)) != 1:
            raise ValueError(
                f"{task_parm_name} of DataFrame has multiple values.")

    def extra_x_time(self, task_param_name: str, method=None):
        if method is None:
            method = lambda x: x
        x = []
        y = []
        for v in self.data.values():
            x.append(v.get("task_params").get(task_param_name))
            y.append(method(v.get("time")))
        return x, y


if __name__ == "__main__":
    import numpy as np
    data = DataFrame('./02.json')
    tasks = data.split_by_tasks()
    tasks[0].filter_task_params(
        'platform', 'cpu').split_by_params('framework')[0].extra_x_time(
            'n_qubit', np.mean)
