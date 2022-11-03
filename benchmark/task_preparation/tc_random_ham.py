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
"""Generate tc random circuit."""

import tensorcircuit as tc
import tensorcircuit.gates as tg


def tc_random_ham(circ: tc.Circuit, n_qubit: int):
    e0 = 0.0
    for i in range(n_qubit - 3):
        e0 += circ.expectation((tg.y(), [i]), (tg.y(), [i + 1]),
                               (tg.y(), [i + 2]), (tg.y(), [i + 3]))
        e0 += circ.expectation((tg.x(), [i]), (tg.x(), [i + 2]))
        e0 += circ.expectation((tg.z(), [i + 1]), (tg.z(), [i + 3]))
        e0 += circ.expectation((tg.z(), [i]), (tg.y(), [i + 1]),
                               (tg.x(), [i + 2]), (tg.z(), [i + 3]))

    return e0


if __name__ == '__main__':
    n_qubit = 5
    circ = tc.Circuit(n_qubit)
    for i in range(n_qubit):
        circ.h(i)
    e0 = tc_random_ham(circ, n_qubit)
    print(e0)
