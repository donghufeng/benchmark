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
"""Benchmark a single gate."""
import argparse

from benchmark import Benchmark

parser = argparse.ArgumentParser()
parser.add_argument("-n",
                    "--file-name",
                    help="file name",
                    type=str,
                    default="0001")
parser.add_argument("-f",
                    "--file-dir",
                    help="file dir",
                    type=str,
                    default="./")
parser.add_argument("-p",
                    "--platform",
                    help="platform",
                    type=str,
                    default="cpu")
parser.add_argument("-q",
                    "--qubit",
                    help="number of qubit",
                    type=int,
                    default=4)
parser.add_argument("-g",
                    "--gate",
                    help="which gate you want to benchmark.",
                    type=str,
                    default='X')
args = parser.parse_args()


def generate_model(platform: str, n_qubits: int, gate: str):
    if platform == 'cpu':
        from mindquantum import benchmark
    elif platform == 'gpu':
        from mindquantum import benchmark_gpu as benchmark
    else:
        raise RuntimeError(f"Unknown backend: {platform}")
    sim = benchmark.benchmark(n_qubits)

    return getattr(sim, f"apply_{gate.upper()}")


def test_single_gate(platform: str, n_qubits: int):
    run = generate_model(platform, n_qubits, args.gate)
    Benchmark(
        args.file_name,
        args.file_dir,
        f"single_gate_{args.gate}",
        {
            "framework": "mindquantum_cpp",
            "platform": platform,
            "n_qubit": n_qubits,
        },
        run,
        warmup=True,
    )


test_single_gate(args.platform, args.qubit)
