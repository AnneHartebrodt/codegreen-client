from datetime import datetime
from urllib.parse import urljoin

import pandas as pd
import requests

from codegreen.config import get_api_endpoint, get_api_key
from codegreen.expections import (InternalServerErrorException,
                                  UnauthorizedException)
from codegreen.utils import process_codecarbon_file


def get_prediction(estimated_runtime_hours:int = 1, 
                   estimated_run_time_in_minutes:int=12,
                   percent_renewable:int=40, 
                   hard_finish_time:datetime.timestamp = datetime.utcnow().replace(hour=18, minute=0, second=0).timestamp(),
                   area_code:list[str] = ['DE'],
                   log_request:bool = True, 
                   process_id:str = None,
                   experiment_name:str = None) -> requests.Response:
    """Get a prediction for an optimal time given the specified parameters.

    :param estimated_runtime_hours: Estimated run time in hours, defaults to 1
    :type estimated_runtime_hours: int, optional
    :param estimated_run_time_in_minutes: Estimated additional minutes of runtime, defaults to 12
    :type estimated_run_time_in_minutes: int, optional
    :param percent_renewable: Required percentage of renewable energy available in the grid at the time of computation, defaults to 40
    :type percent_renewable: int, optional
    :param hard_finish_time: deadline for when the computation needs to be finished, defaults to datetime.utcnow().replace(hour=18, minute=0, second=0).timestamp()
    :type hard_finish_time: datetime.timestamp, optional
    :param area_code: list of area codes with a two letter country code and an optional postal code separated by a dash. Postal codes can be given as 1-5 digit areas. ['CC-PPPPP', 'CC', 'CC-P'], defaults to ['DE']
    :type area_code: list[str], optional
    :param log_request: allow logging the request server side, this is required to compute the carbon offset, defaults to True
    :type log_request: bool, optional
    :param process_id: An string to identify the experiment, defaults to None
    :type process_id: str, optional
    :param experiment_name: Name of the experiment used to load the configuration. If none it will try to load a default configuration, defaults to None
    :type experiment_name: str, optional
    :raises UnauthorizedException: raised when the API key is invalid
    :return: A response object representing the the prediction in the form of a json object, Example: {'optimal_start': 1689703307, 'message': 'No data available', 'avg_percentage_renewable': 0}
    :rtype: requests.Response
    """
    payload = {'estimated_runtime_hours': estimated_runtime_hours, 
               'estimated_runtime_minutes': estimated_run_time_in_minutes,
               'percent_renewable': percent_renewable,
               'hard_finish_time': hard_finish_time,
                'area_code' : area_code,
                'log_request' : log_request,
                'process_id': process_id}
    
    API_URL = get_api_endpoint(experiment_name)
    API_KEY = get_api_key(experiment_name)
    AUTHORIZATION_HEADER = {'Authorization': f'Bearer {API_KEY}', 'content-type': 'application/json'}
    r = requests.post(urljoin(API_URL, 'forecast/timeshift'), json=payload, headers=AUTHORIZATION_HEADER)
    print(r.headers)
    print(r.request)
    if r.status_code == 200:
        return r
    if r.status_code == 401:
        raise UnauthorizedException
    else:
        raise InternalServerErrorException






def submit_nf_resource_usage(trace_file:str, experiment_id:str, task_name:str, experiment_name:str = None)-> requests.Response: 
    """Upload the nextflow report in the trace file. Process id needs to be provided.
    The experiment name can be used to use a specific experiment configuration. Otherwise the experiment
    will be reported under the default settings. 

    :param trace_file: Name of the nextflow trace file to upload.
    :type trace_file: str
    :param process_id: The process id to upload the nextflow report under. Can be used for scoped reporting within an API key scope.
    :type process_id: str
    :param experiment_name: Name of the experiment to report under, defaults to None
    :type experiment_name: str, optional
    :raises UnauthorizedException: will be raised if the API key is invalid or does not exist.
    :return: The response of the server.
    :rtype: requests.Response
    """

    API_URL = get_api_endpoint(experiment_name)
    print(API_URL)
    API_KEY = get_api_key(experiment_name)
    print(API_KEY)
    AUTHORIZATION_HEADER = {'Authorization': API_KEY}
    data = pd.read_csv(trace_file, sep='\t')
    data['task_name'] = task_name

    data['process_id'] = experiment_id

    data.columns = data.columns.str.replace(r"%", "percent_")
    print(data)
    data = data.to_json(orient='records')
    payload = {'submission_type': 'nextflow', 'data': data}
    r = requests.post(urljoin(API_URL, 'reporting'), json=payload, headers=AUTHORIZATION_HEADER)
    
    if r.status_code == 200:
        return r
    else:
        return r
    
#submit_nf_resource_usage('/home/bionets-og86asub/Documents/greenerai/greenerai-client/nf-module/trace-20230614-65123194.txt', task_name='nextflow', experiment_id = 'hashhhhh', experiment_name='my_local_experiment')





def submit_cc_resource_usage(trace_file, process_id, task_name, postal_code='DE-791',experiment_name = None):
    """Upload the codecarbon report in the file specified. Process id needs to be provided.
    The experiment name can be used to use a specific experiment configuration. Otherwise the experiment
    will be reported under the default settings. 

    :param trace_file: Name of the nextflow trace file to upload.
    :type trace_file: str
    :param process_id: The process id to upload the nextflow report under. Can be used for scoped reporting within an API key scope.
    :type process_id: str
    :param task_name: The name of the task to upload the nextflow report under
    :type task_name: str
    :param experiment_name: Name of the experiment to report under, defaults to None
    :type experiment_name: str, optional
    :param postal_code: Can be used to obfuscate the exact location.
    :type postal_code: str
    :raises UnauthorizedException: will be raised if the API key is invalid or does not exist.
    :return: The response of the server.
    :rtype: requests.Response
    """
    
    API_URL = get_api_endpoint(experiment_name)
    API_KEY = get_api_key(experiment_name)
    AUTHORIZATION_HEADER = {'Authorization': API_KEY}
    data = process_codecarbon_file(trace_file, 
                                   process_id= process_id,
                                   task_name=task_name,
                                    postal_code=postal_code)
    print(data)
    data = data.to_json()
    payload = {'submission_type': 'codecarbon', 'data': data}
    r = requests.post(urljoin(API_URL,'reporting'), json=payload, headers=AUTHORIZATION_HEADER)
    if (r.status_code == 200 or r.status_code == 201):
        return r
    else:
        raise UnauthorizedException


def get_data(submission_type:str, dump:bool=False, experiment_name:str = None)-> pd.DataFrame:
    """Retrieve the data submitted to the server. There are currently three options: the codecarbon logs,
    the nextflow logs and the request log for all the requests made to the server.

    :param submission_type: One of ['codecarbon', 'nextflow', 'requests']
    :type submission_type: str
    :param dump: Dump all data, can only be used in combination with an admin API key, defaults to False
    :type dump: bool, optional
    :param experiment_name: Name of the experiment to identify the configuration file by., defaults to None
    :type experiment_name: str, optional
    :raises UnauthorizedException: raised when no valid API key is submitted.
    :return: Returns the data as a Dataframe
    :rtype: pd.DataFrame
    """
    
    API_URL = get_api_endpoint(experiment_name)
    API_KEY = get_api_key(experiment_name)
    AUTHORIZATION_HEADER = {'Authorization': f'Bearer {API_KEY}', 'content-type': 'application/json'}

    print(API_URL)

    r = requests.get(urljoin(API_URL,'data'), headers=AUTHORIZATION_HEADER, params={'submission_type': submission_type, 'dump': dump})
    print(r)
    if r.status_code == 200:
        data = pd.DataFrame(r.json()['data'])
        return data


def get_location_prediction(
        estimated_runtime_hours:int = 1, 
                   estimated_run_time_in_minutes:int=12,
                   percent_renewable:int=40, 
                   hard_finish_time:datetime.timestamp = datetime.utcnow().replace(hour=23, minute=0, second=0).timestamp(),
                   area_code:list[str] = ['DE','FR'],
                   log_request:bool = True, 
                   process_id:str = None,
                   experiment_name:str = None)-> requests.Response:
    """
    Get a preddiction for the optimal location to perform the computation within the given time frame using the specified
    percentage of renewable energy.

    :param estimated_runtime_hours: Run time of the code in hours, defaults to 1
    :type estimated_runtime_hours: int, optional
    :param estimated_run_time_in_minutes: additional run time of the code in minutes, defaults to 12
    :type estimated_run_time_in_minutes: int, optional
    :param percent_renewable: required percentage of renewable energy in the grid at the time of computation, defaults to 40
    :type percent_renewable: int, optional
    :param hard_finish_time: Deadline for the termination of the code, defaults to datetime.utcnow().replace(hour=24, minute=0, second=0).timestamp() which is 24 ahead.
    :type hard_finish_time: datetime.timestamp, optional
    :param area_code: list of potential area codes for the computation, defaults to ['DE','FR']
    :type area_code: list[str], optional
    :param log_request: allow logging the request at the server side, defaults to True
    :type log_request: bool, optional
    :param process_id: process id to scope the project, defaults to None
    :type process_id: str, optional
    :param experiment_name: Name of the experiment to load the correct configuration, defaults to None
    :type experiment_name: str, optional
    :raises UnauthorizedException: Raised if no correct API key is submitted with the request.
    :return: A response in for the request with the content in json format.
    :rtype: requests.Response
    """
    
    API_URL = get_api_endpoint(experiment_name)
    print(API_URL)
    API_KEY = get_api_key(experiment_name)
    print(API_KEY)
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

    return r