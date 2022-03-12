# 3.5 or higher

import subprocess

# TODO query by username first then fetch ID from that

# ID of streamer to be queried
streamer_id = 71092938
# Path to the Twitch CLI
twitch_path = "C:\\Users\\Henning\\scoop\\shims\\twitch.exe"

sub = subprocess.Popen(f"{twitch_path} api get videos -q user_id={streamer_id} -q first=100", shell=True, stdout=subprocess.PIPE)

json_file = open("video_data.json", "w")
json_file.write(sub.stdout.read().decode("utf-8"))
json_file.close()

#TODO get into json structure, pop first if he is live with another query, then save it again