import sys
import re
from datetime import date, datetime
from subprocess import run


users = {}
proc_count = 0
result = run(["ps aux"], shell=True, capture_output=True)
my_stdout = result.stdout.decode("utf-8").split("\n")
my_stdout.pop(len(my_stdout)-1)
mem_total = 0.0
cpu_total = 0.0
mem_max = -1.0
cpu_max = -1.0
mem_max_process_name = ''
cpu_max_process_name = ''
head = 0

for item in my_stdout:
    spl_item = item.split()
    user_name = spl_item[0]
    if user_name == "USER":
        time_str = re.search(r".+TIME\s", item)
        head = len(time_str.group())
        process_name = item[head:]
    else:
        proc_count += 1
        process_name = item[head:]
        cpu = float(spl_item[2])
        cpu_total += cpu
        mem = float(spl_item[3])
        mem_total += mem
        if cpu > cpu_max: cpu_max, cpu_max_process_name = cpu, process_name[:20]
        if mem > mem_max: mem_max, mem_max_process_name = mem, process_name[:20]
        try:
            users[user_name] += 1
        except KeyError:
            users[user_name] = 1
report = "REPORT ABOUT SYSTEM\r\n"
report += f"Processes total: {proc_count}\r\n"
report += "System users: "
for user in list(users.keys()):
    report += user
    report += " "
report += "\r\nProcesses per users: \r\n"
for key, value in users.items():
    report += f"{key} : {value}\r\n"
report += f"Mem in use: {round(mem_total,2)}\r\n"
report += f"CPU in use: {round(cpu_total,2)}\r\n"
report += f"Max Mem process_name: {mem_max_process_name}\r\n"
report += f"Max CPU in use: {cpu_max_process_name}\r\n"
print(report)

current_date_time = datetime.now()
current_time = str(current_date_time.time())[:5]
file_name = f"{date.today()}-{current_time}-scan.txt"
out = sys.stdout
with open(file_name, 'w') as f:
    sys.stdout = f
    print(report)
    sys.stdout = out
