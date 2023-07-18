import functools
from datetime import datetime, timedelta
from codecarbon import track_emissions
import numpy as np
import os.path as op
from http import HTTPStatus
import time
from dateutil import tz
from uuid import uuid4


from codegreen.utils import get_configuration, write_config_file
from codegreen.config import get_api_endpoint, get_api_key
from codegreen.queries import submit_cc_resource_usage, get_prediction, submit_nf_resource_usage, get_data, get_location_prediction
from codegreen.expections import UnauthorizedException, InternalServerErrorException



API_URL = get_api_endpoint()
API_KEY = get_api_key()
AUTHORIZATION_HEADER = {"Authorization": API_KEY}


def time_shift(experiment_name):
    """
    This parametrizable decorator allows to easily time shift any python computation to a later point.
    """

    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            config = get_configuration(experiment_name)
            hard_finish_time =(datetime.now() + timedelta(hours=config['allowed_delay_hours'])).timestamp()
            print(config)
            try:
                sleep_until(
                    estimated_runtime_hours=config["estimated_runtime_hours"],
                    estimated_run_time_in_minutes=config["estimated_runtime_minutes"],
                    percent_renewable=config["percent_renewable"],
                    hard_finish_time=hard_finish_time,
                    area_code=config["area_code"],
                    log_request=config["log_request"],
                    process_id=config["experiment_hash"],
                )
            except KeyError as e:
                print(
                    f"Error: Missing key in config dictionary: {str(e)}, Please initialize your configuration with @init_experiment"
                )

            return func(*args, **kwargs)

        return wrapper

    return actual_decorator


def sleep_until(
    estimated_runtime_hours,
    estimated_run_time_in_minutes,
    percent_renewable,
    hard_finish_time,
    area_code,
    log_request,
    process_id,
):
    """
    This funtion puts your program to sleep until the energy is green enough in your area.
    """
    try:
        print(type(hard_finish_time))
        r = get_prediction(
            estimated_runtime_hours,
            estimated_run_time_in_minutes,
            percent_renewable,
            hard_finish_time,
            area_code,
            log_request,
            process_id,
        )
        if r.status_code == HTTPStatus.UNAUTHORIZED:
            raise UnauthorizedException
        if r.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
            raise InternalServerErrorException
        print(r.request)
        js = r.json()
        print(js)
        sleep_until = js["suggested_start"]

        sleep_until = datetime.utcfromtimestamp(sleep_until)
        sleep_until = sleep_until.replace(tzinfo=tz.tzutc())
        sleep_until = sleep_until.astimezone(tz.tzlocal())
        print(sleep_until)
        print(f"{js['message']}: {sleep_until}")
        print(sleep_until.timestamp())
        sleep_time = sleep_until.timestamp() - datetime.now().timestamp()
        if sleep_time > 0:
            time.sleep(sleep_time)
    except ConnectionError:
        print("Error contacting API")
    except UnauthorizedException:
        print("Unauthorized -- Did you forget to submit the correct API key?")
    except InternalServerErrorException:
        print(
            "Internal server error -- It is most likely not your fault. If this problem persisits please file an issue on Github"
        )


def upload_nf_report(experiment_name):
    """
    This parametrizable decorator allows to easily upload an execution report to the web
    """

    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args):
            config = get_configuration(experiment_name)
            try:
                r = submit_nf_resource_usage(config["nexflow_logfile"], process_id=config["experiment_hash"])
            except KeyError as e:
                print(
                    f"Error: Missing key in config dictionary: {str(e)}, Please initialize your configuration with @init_experiment"
                )

            print(r.status_code)
            return func(*args)

        return wrapper

    return actual_decorator


def upload_cc_report(experiment_name):
    """
    This parametrizable decorator allows to easily upload an execution report to the web.
    
    """

    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args):
            func(*args)

            print("Uploading")
            config = get_configuration(experiment_name)
            try:
                r = submit_cc_resource_usage(
                    config["codecarbon_logfile"], process_id=config["experiment_hash"], task_name=config['experiment_name'], postal_code=config["area_code"]
                )
            except KeyError as e:
                print(
                    f"Error: Missing key in config dictionary: {str(e)}, Please initialize your configuration with @init_experiment"
                )
            print(r.status_code)
        return wrapper

    return actual_decorator


def init_experiment(
    experiment_name,
    nextflow_logfile,
    area_code,
    estimated_runtime_hours,
    estimated_runtime_minutes,
    codecarbon_logfile='emissions.csv',
    percent_renewable=30,
    allowed_delay_hours=24,
    log_request=True,
    overwrite=False,
):
    """
    This parametrizable decorator allows to easily upload an execution report to the web
    """

    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args):
            write_config_file(
                experiment_name=experiment_name,
                codecarbon_logfile=codecarbon_logfile,
                nextflow_logfile=nextflow_logfile,
                area_code=area_code,
                estimated_runtime_hours=estimated_runtime_hours,
                estimated_runtime_minutes=estimated_runtime_minutes,
                percent_renewable=percent_renewable,
                allowed_delay_hours=allowed_delay_hours,
                log_request=log_request,
                overwrite=overwrite,
            )
            return func(*args)

        return wrapper
    return actual_decorator

if __name__=='__main__':
    @init_experiment(estimated_runtime_hours=1,estimated_runtime_minutes=30,percent_renewable=40,allowed_delay_hours= 24, area_code="DE-9",log_request=True,experiment_name="my_experiment",codecarbon_logfile="experiment.log",nextflow_logfile="nextflow.log",overwrite=True)
    @time_shift("my_experiment")
    @upload_cc_report("my_experiment")
    @track_emissions(output_file='experiment.log')
    def hello_random_matrix_generator():
        for _ in range(1000):
            np.random.random((1000, 1000))


    hello_random_matrix_generator()
    



    data = get_data('codecarbon', False)

    print(API_KEY)
    print(AUTHORIZATION_HEADER)
    
    pred = get_location_prediction(estimated_runtime_hours = 1, estimated_run_time_in_minutes=12,percent_renewable=40, hard_finish_time = datetime.utcnow().replace(hour=18, minute=0, second=0).timestamp(),area_code = ['DE-79117', 'CY-1', 'CZ-8'] ,log_request = True, process_id = '1')
    print(pred.json())