#! /bin/bash

# Copyright 2022 Huawei Technologies Co., Ltd
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

BASEPATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && pwd )
ROOTDIR="$BASEPATH"
python_venv_path="${ROOTDIR}/venv"
third_party="${ROOTDIR}/third_party"

# ------------------------------------------------------------------------------

# Locate python or python3
. "$ROOTDIR/env_scripts/locate_python3.sh"

# ------------------------------------------------------------------------------

# Activate virtual python
. "$ROOTDIR/env_scripts/python_virtualenv_activate.sh"

. "$ROOTDIR/env_scripts/install_benchmark_lib.sh"

export PYTHONPATH=$ROOTDIR/benchmark:$PYTHONPATH
