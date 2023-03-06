# Fetches the timestamps of all the videos of a streamer, when they start and end as a tuple with unix timestamps

import subprocess # For running the Twitch CLI
import dateutil.parser # For easy ISO8601 conversion
import json
from typing import List, Tuple # Type hinting

# TODO query by username first then fetch ID from that

# Path to the Twitch CLI
# twitch_path = ""

def convert_duration_time_to_seconds(time_string: str) -> int:
    # Format is 00h00m00s
    time_string = time_string.replace("h", ":")
    time_string = time_string.replace("m", ":")
    time_string = time_string.replace("s", "")
    time_list = time_string.split(":")
    time_list = [int(i) for i in time_list]
    time_list.reverse()
    seconds = 0
    for i in range(len(time_list)):
        seconds += time_list[i] * 60 ** i
    return seconds

def iso8601_to_unix(iso8601_string: str) -> int:
    # Format is 2021-05-31T20:00:00Z
    return int(dateutil.parser.isoparse(iso8601_string).timestamp())

def get_streaming_timestamps(streamer_id: int) -> List[Tuple[int, int]]:
    # TODO add support for the after=cursor query parameter for pagination
    sub = subprocess.Popen(f"twitch.exe api get videos -q user_id={streamer_id} -q first=100", shell=True, stdout=subprocess.PIPE, encoding="utf-8")

    json_file = open("video_data.json", "w", encoding="utf-8")
    json_file.write(sub.stdout.read())
    json_file.close()

    data = {} # Placeholder
    with open("video_data.json", "r", encoding="utf-8") as json_file:
        data: dict = json.load(json_file)

    stream_durations: List[Tuple[int, int]] = [] # List of tuples of (video_id, duration in seconds)

    # The data key of the json file is a python list of all the videos 
    for dict in data["data"]:
        # Each attribute is a key in the video dictionary
        end_time = iso8601_to_unix(dict["created_at"])
        duration = convert_duration_time_to_seconds(dict["duration"])
        # Tuple of the start timestamp and end timestamp
        stream_durations.append((end_time-duration, end_time))

    #TODO get into json structure, pop first if he is live with another query, then save it again
    
    return stream_durations


if __name__ == "__main__":
    # ID of streamer to be queried
    streamer_id = 71092938
    print(get_streaming_timestamps(streamer_id))
