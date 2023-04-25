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
from mindquantum import *


def mq_qft_prepare(backend:str, n_qubits: str):
    backend = {'cpu':'mqvector','gpu':'mqvector_gpu'}[backend]
    circ = qft(range(n_qubits))
    sim = Simulator(backend, n_qubits)
    circ.get_cpp_obj()

    def run():
        sim.apply_circuit(circ)
        return sim

    return run
