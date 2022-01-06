import os
import argparse
import re
import json

parser = argparse.ArgumentParser(description='Process access.log')

parser.add_argument('-f', dest='file', action='store', help='Path to logfile')
args = parser.parse_args()
path_log = args.file

files = []
REQUEST_INFO_KEYS = ["IP", "URL", "Method", "Duration", "Date", "Time"]

if os.path.isfile(path_log):
    files = [path_log]
elif os.path.isdir(args.file):
    all_files = os.listdir(path_log)
    files = list(filter(lambda f: f.endswith(".log"), all_files))
    os.chdir(path_log)


for file in files:
    top_reqs_qty = []
    top_req_durations = []
    dict_ip = {}
    dict_requests_by_methods = {"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0, "HEAD": 0, "OPTIONS": 0}
    data = {"Source file": file}
    file_res = file.replace(".log", ".res")

    with open(file) as my_file:
        ind = 0
        for line in my_file:
            ind += 1
            ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            url_match = re.search(r"\"http://[0-9a-z./-]+\"", line)
            if url_match:
                url = url_match.group(0)[1:-1]
            else:
                url = "-"
            method_match = re.search(r"\] \"(POST|GET|PUT|DELETE|HEAD|OPTIONS)", line)
            date_time_match = re.search(r"\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}", line)
            if method_match is not None:
                method = method_match.group(1)
                dict_requests_by_methods[method] += 1
            if ip_match is not None:
                ip = ip_match.group()
                try:
                    dict_ip[ip] += 1
                except KeyError:
                    dict_ip[ip] = 1
            line_spl = line.split(" ")
            line_spl.reverse()
            duration = int(line_spl[0])
            date = date_time_match.group()[0:11]
            time = date_time_match.group()[12:20]
            values = [ip, url, method, duration, date, time]
            req_info = dict(zip(REQUEST_INFO_KEYS, values))

            top_req_durations.append(req_info)
            if len(top_req_durations) > 3:
                top_req_durations.sort(reverse=True, key=lambda el: el["Duration"])
                top_req_durations.pop()

    list_keys = list(dict_ip.keys())
    for key in list_keys:
        ip_data = {"IP": key, "req_n": dict_ip[key]}
        top_reqs_qty.append(ip_data)
        if len(top_reqs_qty) > 3:
            top_reqs_qty.sort(reverse=True, key=lambda el: el["req_n"])
            top_reqs_qty.pop()

    data["Total requests"] = ind
    data["Requests by Method"] = dict_requests_by_methods
    data["Top 3 requests quantity IP's"] = top_reqs_qty
    data["Top 3 duration requests"] = top_req_durations
    print(json.dumps(data, indent=4))
    with open(file_res, 'w') as outfile:
        json.dump(data, outfile)
