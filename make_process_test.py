from os import sched_get_priority_max
import pandas as pd
import os

out_dir = "process"
if not os.path.isdir(out_dir):
    os.makedirs(out_dir)

book = pd.ExcelFile("sample_format.xlsx")
sheet = book.sheet_names
target = sheet[-1]

df = book.parse(sheet_name=target)

middle_tables = df["Middle Table"].to_list()
processes = df["Process"].to_list()
sources = df["Sources"].to_list()
outputs = df["output"].to_list()

txt = "```plantuml\n@startuml\ntop to bottom direction\n"
for process in processes:
    if "join" not in str(process):
        continue
    txt += f"() {process}\n"
txt += "\n"

self_list = []
for i in range(len(processes)):
    if "self" in sources[i]:
        source = sources[i].split(",")
        for s in source:
            if not s in self_list:
                self_list.append(s)
for l in self_list:
    txt += f'entity "{l}"' + '{}\n'
txt += "\n"


n_process = len(processes)
for i in range(n_process):
    if "join" not in str(processes[i]):
        txt += f"{sources[i]} --|> {outputs[i]}\n"
    else:
        source = sources[i].split(",")
        for s in source:
            txt += f"{s} --|>{processes[i]}\n"
    
with open(f"{out_dir}/sample_process.md", "w") as f:
    txt += "@enduml"
    f.write(txt)