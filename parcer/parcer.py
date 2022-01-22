import sys
import re
from datetime import date, datetime
from subprocess import run


users = {}
proc_count = 0
# result = run(["ps aux | grep python"], shell=True, capture_output=True)
result = run(["ps aux"], shell=True, capture_output=True)
my_stdout = result.stdout.decode("utf-8").split("\n")
my_stdout.pop(len(my_stdout)-1)
mem_total = 0.0
cpu_total = 0.0
mem_max = 0.0
cpu_max = 0.0
mem_max_process_name = ''
cpu_max_process_name = ''

for item in my_stdout:
    user_name = re.search(r"\S+\s", item)
    user_name = user_name.group()
    if user_name != "USER ":
        proc_count += 1
        time_str = re.search(r".+:[0-9][0-9]\s+[0-9]+:[0-9][0-9]\s", item)
        head = len(time_str.group())
        process_name = item[head:]
        start_str = re.search(r"\S+\s+[0-9]+\s", item)
        head = len(start_str.group())
        cpu = float(item[head:head+4])
        cpu_total += cpu
        mem = float(item[head+5:head+9])
        mem_total += mem
        if cpu > cpu_max:
            cpu_max = cpu
            cpu_max_process_name = process_name[:20]
        if mem > mem_max:
            mem_max = mem
            mem_max_process_name = process_name[:20]
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
report += f"Mem in use: {mem_total}\r\n"
report += f"CPU in use: {cpu_total}\r\n"
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
