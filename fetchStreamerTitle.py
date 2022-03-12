# 3.5 or higher

import subprocess
import json

# ID of streamer to be queried
streamer_id = 71092938
# Path to the Twitch CLI
twitch_path = "C:\\Users\\Henning\\scoop\\shims\\twitch.exe"

sub = subprocess.Popen(f"{twitch_path} api get videos -q user_id={streamer_id} -q first=100", shell=True, stdout=subprocess.PIPE)

data = json.loads(sub.stdout.read().decode("utf-8"))

file = open("titles.txt", "w")

lines = []
for i in data["data"]:
    lines.append(i["title"] + "\n")

file.writelines(lines)
file.close()

#TODO opening the files twice, bad
with open("titles.txt", 'r+') as fd:
    lines = fd.readlines()
    fd.seek(0)
    fd.writelines(line for line in lines if line.strip())
    fd.truncate()
