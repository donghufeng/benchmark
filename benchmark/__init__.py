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
# ============================================================================
"""Benchmark of mindquantum."""
import importlib as _importlib
import json
import os
from typing import Dict

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
CONFIG_JSON = os.path.join(PROJECT_PATH, "benchmark/config.json")
TMP_PATH = os.path.join(PROJECT_PATH, "tmp")
if not os.path.exists(TMP_PATH):
    os.mkdir(TMP_PATH)


def get_y(x: int, x0: int, y0: int, x1: int, y1: int) -> int:
    return int(y0 - 1.0 * (x - x0) * (y0 - y1) / (x1 - x0))


def get_config(task_name: str) -> Dict:
    with open(CONFIG_JSON) as f:
        config = json.load(f)
    if task_name not in config:
        raise ValueError(f"Task {task_name} not in config file.")
    return config[task_name]


SEED = get_config("global_seed")

from .src import Benchmark, BenchmarkProcess, DataFrame, Task, TaskManage

__all__ = [
    "BenchmarkProcess",
    "Benchmark",
    "Task",
    "TaskManage",
    "DataFrame",
]
__all__.sort()
