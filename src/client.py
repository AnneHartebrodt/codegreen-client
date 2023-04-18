import requests
import time
from datetime import timedelta, datetime, timezone
import functools
import pandas as pd

AUTHORIZATION_HEADER = {'Authorization': 
           'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2ODAwOTcwMTIsInN1YiI6IjMxOThmMjVlLWRhNWEtNDI3ZC1iMDQwLWJlNDM4MDA1YzQ1NSJ9.rWR75a__ArEqeD28AorSLsOXHzO_iXVbjCrnzH2eBb4'}

trace_file = '/home/bionets-og86asub/Documents/netmap/workflows/pipeline_trace.txt'

def get_prediction(estimated_runtime_hours = 1, 
                   estimated_run_time_in_minutes=12,
                   percent_renewable=40, 
                   hard_finish_time = datetime.now().replace(hour=18, minute=0, second=0),
                   area_code = 'DE-79117',
                   headers=AUTHORIZATION_HEADER):
    payload = {'estimated_runtime_hours': estimated_runtime_hours, 
               'estimated_runtime_minutes': estimated_run_time_in_minutes,
               'percent_renewable': percent_renewable,
               'hard_finish_time': hard_finish_time.strftime('%Y-%m-%d %H:%M'),
                'area_code' : area_code }

    r = requests.post('http://localhost:5000/api/v1/data/prediction', json=payload, headers=headers)
    return r



def validate_request_parameters(payload):
    # should we validate the requests before sending them to the API
    # Probably a good idea, but what is the expected behaviour in the 
    # code then?
    return True


def submit_workflow_ressource_usage(trace_file, workflow_engine):
    data = pd.read_csv(trace_file, sep='\t')
    data = data.to_json()
    payload = {'workflow_engine': workflow_engine, 'report': data}
    r = requests.post('http://localhost:5000/api/v1/data/workflow', json=payload, headers=AUTHORIZATION_HEADER)
    return r

submit_workflow_ressource_usage(trace_file, workflow_engine='nextflow')

def sleep_until(estimated_runtime_hours, estimated_run_time_in_minutes, percent_renewable, hard_finish_time, area_code, headers):
    """
    This funtion puts your program to sleep until the energy is green enough in your area.
    """
    try:
        r = get_prediction(estimated_runtime_hours, estimated_run_time_in_minutes, percent_renewable, hard_finish_time, area_code, headers)
        js = r.json()
        sleep_until = js["suggested_start"]
        sleep_until = datetime.fromtimestamp(sleep_until)
        print(f"{js['message']}: {sleep_until}")
        sleep_time = sleep_until.timestamp() - datetime.now().timestamp()
        if sleep_time > 0:
            time.sleep(sleep_time)
    except RuntimeError:
        print('error')
        pass


def await_computation(estimated_runtime_hours, estimated_run_time_in_minutes, percent_renewable, hard_finish_time, area_code, headers):
    """
    This parametrizable decorator allows to easily time shift any python computation to a later point.
    """
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Anything can go wrong, so let's put it in a try block
            sleep_until(estimated_runtime_hours, estimated_run_time_in_minutes, percent_renewable, hard_finish_time, area_code, headers)
            return func(*args, **kwargs)
        return wrapper
    return actual_decorator


@await_computation(estimated_runtime_hours=1, estimated_run_time_in_minutes=12, percent_renewable=20, hard_finish_time=datetime.now().replace(hour=23, minute=0, second=0), area_code='DE-791', headers=AUTHORIZATION_HEADER)
def hello_world():
    print('Thank you for being carbon aware')


r = get_prediction(headers=AUTHORIZATION_HEADER)
r.json()

hello_world()