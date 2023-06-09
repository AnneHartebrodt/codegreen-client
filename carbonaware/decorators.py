import functools
from datetime import datetime
from codecarbon import track_emissions
import numpy as np
import os.path as op
from carbonaware.queries import submit_resource_usage, get_prediction
from carbonaware.expections import UnauthorizedException, InternalServerErrorException
from http import HTTPStatus
import time


def await_computation(headers, estimated_runtime_hours, estimated_run_time_in_minutes, percent_renewable, hard_finish_time, area_code, log_request=True):
    """
    This parametrizable decorator allows to easily time shift any python computation to a later point.
    """
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Anything can go wrong, so let's put it in a try block
            sleep_until(headers, estimated_runtime_hours, estimated_run_time_in_minutes, percent_renewable, hard_finish_time, area_code, log_request)
            return func(*args, **kwargs)
        return wrapper
    return actual_decorator


def sleep_until(headers, estimated_runtime_hours, estimated_run_time_in_minutes, percent_renewable, hard_finish_time, area_code, log_request):
    """
    This funtion puts your program to sleep until the energy is green enough in your area.
    """
    try:
        print(type(hard_finish_time))
        r = get_prediction(headers, estimated_runtime_hours, estimated_run_time_in_minutes, percent_renewable, hard_finish_time, area_code, log_request)
        if r.status_code == HTTPStatus.UNAUTHORIZED:
            raise UnauthorizedException
        if r.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
            raise InternalServerErrorException
        js = r.json()
        sleep_until = js["suggested_start"]
        sleep_until = datetime.fromtimestamp(sleep_until)
        print(f"{js['message']}: {sleep_until}")
        sleep_time = sleep_until.timestamp() - datetime.now().timestamp()
        if sleep_time > 0:
            time.sleep(sleep_time)
    except ConnectionError:
        print('Error contacting API')
    except UnauthorizedException:
        print('Unauthorized -- Did you forget to submit the correct API key?')
    except InternalServerErrorException:
        print('Internal server error -- It is most likely not your fault. If this problem persisits please file an issue on Github')
    except Exception:
        print('Other error occurred')



def upload_report(header, trace_file, submission_type, **kwargs):
    """
    This parametrizable decorator allows to easily upload an execution report to the web
    """
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print('Uploading')
            r = submit_resource_usage(header=header, trace_file=trace_file, submission_type=submission_type, **kwargs)
            return func(*args, **kwargs)
        return wrapper
    return actual_decorator

AUTHORIZATION_HEADER = {'Authorization': 
           'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2ODYzMTMzMzMsInN1YiI6Ijc3Y2ZkYjUyLTA2NjAtNDg1OS1hNzZhLTdhOTBiYjdiMjQ5YiIsInNjb3BlIjoiVGVzdCBwcm9qZWN0In0.yWLrwWT2xCz4szC0i9f0BGBifl3XXLU9FfG1fKseq08'}


@track_emissions
@await_computation(headers=AUTHORIZATION_HEADER, estimated_runtime_hours=1, estimated_run_time_in_minutes=12, percent_renewable=30, hard_finish_time=datetime.now().replace(hour=23, minute=0, second=0), area_code='DE-791', log_request=True)
def hello_world():
    print('Thank you for being carbon aware')


filename='/home/bionets-og86asub/Documents/greenerai/greenerai-client/emissions.csv'
bn = op.basename(filename)
additional_args = {'task_name': 'test',  'task_hash' : '123',  'postal_code':'DE-791'} 
@track_emissions(output_file=bn)
@await_computation(headers=AUTHORIZATION_HEADER, estimated_runtime_hours=1, estimated_run_time_in_minutes=12, percent_renewable=30, hard_finish_time=datetime.now().replace(hour=23, minute=0, second=0), area_code='DE-791', log_request=True)
@upload_report(header = AUTHORIZATION_HEADER, trace_file=filename, submission_type='codecarbon', **additional_args)
def hello_random_matrix_generator():
    for _ in range(1000):
        np.random.random((1000, 1000))



hello_random_matrix_generator()



