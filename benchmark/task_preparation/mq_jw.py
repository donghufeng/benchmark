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
"""Generate mq random fermion jordan wigner transformation."""

from mindquantum.core.operators import FermionOperator
from mindquantum.algorithm.nisq.chem import Transform


def random_fermion(n_qubit: int) -> FermionOperator:
    out = FermionOperator()
    for i in range(n_qubit - 3):
        out += FermionOperator(f"{i} {i+1}^ {i+2} {i+3}^")
        out += FermionOperator(f"{i}^ {i+2}^")
        out += FermionOperator(f"{i+1} {i+3}")
        out += FermionOperator(f"{i} {i+1} {i+2}^ {i+3}^")
    return out


if __name__ == "__main__":
    fo = random_fermion(5)
    jw_trans = Transform(fo).jordan_wigner
    jw_trans()
