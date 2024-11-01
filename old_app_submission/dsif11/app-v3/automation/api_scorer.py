######################################################################
# Scores a list of input files using fastapi
######################################################################
import requests
import json5

def score_api(file_list:list):

    url = "http://127.0.0.1:8000/predict_automation"
    headers = {'content-type': 'application/json'}
    requests.post(url, data=json5.dumps(file_list), headers=headers)

    return None

