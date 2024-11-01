import os
from datetime import datetime
from api_scorer import score_api
import time
import sys
sys.path.insert(0, '../src/')
sys.path.insert(0, '../data')
sys.path.insert(0, '../')

from conf.conf import landing_path_input_data

# scan frequency
scan_freq_seconds = 5

# initial file scan
files_earlier = []
files_now = os.listdir(landing_path_input_data)

# Infinite loop, will continue until user types ctrl-C to quit the application
while True:
    if len(files_now) > len(files_earlier):
        print("New transactions detected. Time:", datetime.now())
        # list files to process
        to_process = [x for x in files_now if x not in files_earlier]
        print("Processing files: ", to_process)

        # update list
        files_earlier = files_now

        # call api with new file
        score_api(to_process)

    files_now = os.listdir(landing_path_input_data)
    time.sleep(scan_freq_seconds)