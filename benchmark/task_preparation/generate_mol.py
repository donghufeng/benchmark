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
"""Generate molecule data."""

import os

from openfermion.chem import MolecularData
from openfermionpyscf import run_pyscf
from mindquantum.algorithm.nisq.chem import generate_uccsd

from benchmark import TMP_PATH, get_config


def generate_molecule_data(geometry, file_name, file_path):
    name = os.path.join(TMP_PATH, file_name + ".hdf5")
    if os.path.exists(name):
        mole_of = MolecularData(filename=name)
        mole_of.load()
    else:
        basis = "sto3g"
        mole_of = MolecularData(geometry, basis, multiplicity=1, filename=name)
        mole_of = run_pyscf(mole_of, run_ccsd=1, run_fci=1, run_scf=1)
        mole_of.save()
    return mole_of


def generate_vqe_circ_and_ham(mole_name):
    task_name = 'vqe'
    config = get_config(task_name)
    geometry = config[mole_name]
    mole = generate_molecule_data(geometry, mole_name, TMP_PATH)
    circ, _, _, qo, _, _ = generate_uccsd(mole)
    return circ, qo
