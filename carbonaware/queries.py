import requests
from datetime import datetime
import pandas as pd
from carbonaware.utils import process_codecarbon_file



def get_prediction(header,
        estimated_runtime_hours = 1, 
                   estimated_run_time_in_minutes=12,
                   percent_renewable=40, 
                   hard_finish_time = datetime.now().replace(hour=18, minute=0, second=0),
                   area_code = 'DE-79117',
                   log_request = True):
    payload = {'estimated_runtime_hours': estimated_runtime_hours, 
               'estimated_runtime_minutes': estimated_run_time_in_minutes,
               'percent_renewable': percent_renewable,
               'hard_finish_time': hard_finish_time.strftime('%Y-%m-%d %H:%M'),
                'area_code' : area_code,
                'log_request' : log_request}

    r = requests.post('http://localhost:5000/api/v1/data/prediction', json=payload, headers=header)
    return r




def submit_resource_usage(header, trace_file, submission_type):
    if submission_type  == 'codecarbon':
        data = process_codecarbon_file(trace_file, 'lsalkasdp-fa1082', 'data_content', '90')
    elif submission_type == 'nextflow':
        data = pd.read_csv(trace_file, sep='\t')
        data = data.to_json()
    payload = {'submission_type': submission_type, 'data': data}
    r = requests.post('http://localhost:5000/api/v1/data/reporting', json=payload, headers=header)
    return r 