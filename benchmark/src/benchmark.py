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
# ============================================================================
"""Benchmark class"""
import argparse
import json
import os
import time

MAX_ITER = 100
MAX_TIME = 2


class Benchmark:
    def __init__(
        self,
        file_name,
        file_path,
        task_name,
        task_params,
        task_fun,
        *task_args,
        warmup=True,
    ):
        self.file_name = file_name
        self.file_path = os.path.abspath(file_path)
        self.task_name = task_name
        self.task_params = task_params
        self.task_fun = task_fun
        self.task_args = task_args
        self.data = {
            "task_name": self.task_name,
            "task_params": self.task_params,
        }
        self.task_id = f"{self.task_name}: {self.task_params}"
        self.warmup = warmup
        self.run()
        self.save()

    def run(self):
        task_desc = ",\t".join(
            f"{arg_name}: \033[1;37m{arg_val}\033[00m"
            for arg_name, arg_val in self.task_params.items()
        )
        print(
            f"runing task \033[1;36m{self.task_name}\033[00m with {task_desc}. ",
            end="\t",
        )
        if self.warmup:
            self.task_fun(*self.task_args)
        t = [time.time()]
        self.data["start time"] = time.ctime()
        n_step = 0
        while True:
            self.task_fun(*self.task_args)
            this_t = time.time()
            t.append(this_t)
            if this_t - t[0] > MAX_TIME or n_step > MAX_ITER:
                break
            n_step += 1
        t = [j - t[0] for j in t[1:]]
        self.data["time"] = t
        self.data["mean"] = sum(t) / len(t)
        print(f"mean time: \033[4;31m{self.data['mean']}\033[00m")

    def save(self):
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)
        file_poi = os.path.join(self.file_path, self.file_name + ".json")
        data = {}
        if os.path.exists(file_poi):
            with open(file_poi, "r") as f:
                data = json.load(f)
        data[self.task_id] = self.data
        with open(file_poi, "w") as f:
            json.dump(data, f, indent=4)


class BenchmarkProcess:
    def __init__(self, file_name, file_dir="./"):
        import pandas as pd

        self.file_name = file_name
        self.file_dir = file_dir
        file_poi = os.path.join(os.path.abspath(file_dir), file_name + ".json")
        with open(file_poi, "r") as f:
            self.data = json.load(f)
        self.tasks_data = {}
        for _, task_data in self.data.items():
            task_name = task_data["task_name"]
            if task_name not in self.tasks_data:
                self.tasks_data[task_name] = []
            self.tasks_data[task_name].append(task_data)
        self.meta_data = {}
        for task in self.tasks_data:
            task_datas = self.tasks_data[task]
            title = list(task_datas[0]["task_params"].keys())
            title.append("mean")
            data = []
            for d in task_datas:
                data.append(list(d["task_params"].values()))
                data[-1].append(d["mean"])
            data = pd.DataFrame(data, columns=title)
            self.meta_data[task] = data


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    color = ["y", "k", "b", "g"]
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--file-name", help="file name", type=str, default="0001")
    args = parser.parse_args()
    b = BenchmarkProcess(args.file_name)
    for task_name, tasks in b.meta_data.items():
        fig, ax = plt.subplots()
        for idx, g in enumerate(tasks.groupby("simulator")):
            ax.plot(g[1]["n_qubit"], g[1]["mean"], "--", label=g[0], color=color[idx])
            ax.plot(g[1]["n_qubit"], g[1]["mean"], ".", color=color[idx], ms=10)
            ax.set_title(task_name)
            ax.set_xlabel("n_qubit")
            ax.set_ylabel("time")
            ax.set_yscale("log")
            plt.legend()
        print(f"Plotting {task_name}")
        plt.show()
