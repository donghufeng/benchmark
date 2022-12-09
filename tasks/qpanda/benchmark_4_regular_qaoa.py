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
"""Benchmark 4 regular graph maxcut for qpanda."""
import argparse

from benchmark import Benchmark
from benchmark.task_preparation.qpanda_4_regular_model import qpanda_qaoa_prepare

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--file-name", help="file name", type=str, default="0001")
parser.add_argument("-f", "--file-dir", help="file dir", type=str, default="./")
parser.add_argument("-p", "--platform", help="platform", type=str, default="cpu")
parser.add_argument("-q", "--qubit", help="number of qubit", type=int, default=4)
args = parser.parse_args()


def test_4_regular_qaoa(platform: str, n_qubits: int):
    if platform in ["cpu", "gpu"]:
        run = qpanda_qaoa_prepare(platform, n_qubits)
    else:
        raise RuntimeError(
            f"Platform unknown: test_4_regular_qaoa({platform}, {n_qubits})"
        )
    Benchmark(
        args.file_name,
        args.file_dir,
        "4_regular_maxcut",
        {
            "framework": "qpanda",
            "platform": platform,
            "n_qubit": n_qubits,
        },
        run,
        warmup=True,
    )


test_4_regular_qaoa(args.platform, args.qubit)
