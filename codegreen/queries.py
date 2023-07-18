import requests
from datetime import datetime, timezone
import pandas as pd
import requests
from datetime import datetime  
import pandas as pd
from urllib.parse import urljoin

from codegreen.config import get_api_endpoint, get_api_key
from codegreen.utils import process_codecarbon_file

from codegreen.expections import UnauthorizedException


def get_prediction(estimated_runtime_hours = 1, 
                   estimated_run_time_in_minutes=12,
                   percent_renewable=40, 
                   hard_finish_time = datetime.utcnow().replace(hour=18, minute=0, second=0).timestamp(),
                   area_code = 'DE-79117',
                   log_request = True, 
                   process_id = None,
                   experiment_name = None):
    payload = {'estimated_runtime_hours': estimated_runtime_hours, 
               'estimated_runtime_minutes': estimated_run_time_in_minutes,
               'percent_renewable': percent_renewable,
               'hard_finish_time': hard_finish_time,
                'area_code' : area_code,
                'log_request' : log_request,
                'process_id': process_id}
    
    API_URL = get_api_endpoint()
    API_KEY = get_api_key(experiment_name)
    AUTHORIZATION_HEADER = {'Authorization': API_KEY}
    r = requests.post(urljoin(API_URL, 'forecast/timeshift'), json=payload, headers=AUTHORIZATION_HEADER)
    if r.status_code == 200:
        return r
    else:
        raise UnauthorizedException


def submit_nf_resource_usage( trace_file, process_id, experiment_name = None): 
    """
    Submit the nextflow report
    """

    API_URL = get_api_endpoint()
    API_KEY = get_api_key(experiment_name)
    AUTHORIZATION_HEADER = {'Authorization': API_KEY}
    data = pd.read_csv(trace_file, sep='\t')
    data['process_id'] = process_id
    data = data.to_json()
    payload = {'submission_type': 'nextflow', 'data': data}
    r = requests.post(urljoin(API_URL, 'reporting'), json=payload, headers=AUTHORIZATION_HEADER)
    if r.status_code == 200:
        return r
    else:
        raise UnauthorizedException


def submit_cc_resource_usage(trace_file, process_id, task_name, postal_code='DE-791',experiment_name = None):
    
    API_URL = get_api_endpoint()
    API_KEY = get_api_key(experiment_name)
    AUTHORIZATION_HEADER = {'Authorization': API_KEY}
    data = process_codecarbon_file(trace_file, 
                                   process_id= process_id,
                                   task_name=task_name,
                                    postal_code=postal_code)
    data = data.to_json()
    payload = {'submission_type': 'codecarbon', 'data': data}
    r = requests.post(urljoin(API_URL,'reporting'), json=payload, headers=AUTHORIZATION_HEADER)
    if (r.status_code == 200 or r.status_code == 201):
        return r
    else:
        raise UnauthorizedException


def get_data(submission_type, dump=False, experiment_name = None):
    
    API_URL = get_api_endpoint()
    API_KEY = get_api_key(experiment_name)
    AUTHORIZATION_HEADER = {'Authorization': API_KEY}

    r = requests.get(urljoin(API_URL,'data'), headers=AUTHORIZATION_HEADER, params={'submission_type': submission_type, 'dump': dump})
    if r.status_code == 200:
        data = pd.DataFrame(r.json()['data'])
        return data
    else:
        raise UnauthorizedException

def get_location_prediction(
        estimated_runtime_hours = 1, 
                   estimated_run_time_in_minutes=12,
                   percent_renewable=40, 
                   hard_finish_time = datetime.utcnow().replace(hour=18, minute=0, second=0).timestamp(),
                   area_code = 'DE-79117',
                   log_request = True, 
                   process_id = None,
                   experiment_name = None):
    
    API_URL = get_api_endpoint()
    API_KEY = get_api_key(experiment_name)
    AUTHORIZATION_HEADER = {'Authorization': API_KEY}
    payload = {'estimated_runtime_hours': estimated_runtime_hours, 
               'estimated_runtime_minutes': estimated_run_time_in_minutes,
               'percent_renewable': percent_renewable,
               'hard_finish_time': hard_finish_time,
                'area_code' : area_code,
                'log_request' : log_request,
                'process_id': process_id}
    print(payload)
    r = requests.post(urljoin(API_URL, 'forecast/locationshift'), json=payload, headers=AUTHORIZATION_HEADER)
    if r.status_code == 200:
        return r
    else:
        raise UnauthorizedException
    