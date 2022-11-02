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
import os
import json
from typing import Dict

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
CONFIG_JSON = os.path.join(PROJECT_PATH, "benchmark/config.json")


def get_y(x: int, x0: int, y0: int, x1: int, y1: int) -> int:
    return int(y0 - 1.0*(x - x0) * (y0 - y1) / (x1 - x0))


def get_config(task_name: str) -> Dict:
    with open(CONFIG_JSON) as f:
        config = json.load(f)[task_name]
    return config

SEED = get_config('global_seed')

from . import task_preparation
