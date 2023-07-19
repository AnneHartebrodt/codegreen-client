
import pandas as pd
import configparser
from pathlib import Path
import os.path as op
from datetime import datetime, timedelta
import time
from uuid import uuid4
from codegreen.logger import logger
from codegreen.expections import ConfigNotFoundException

def process_codecarbon_file(filename, process_id, task_name, postal_code)-> pd.DataFrame:
    """
    Read file and remove longitude and latitude from file.
    """
    data = pd.read_csv(filename, sep=',', header=0)


    data = data[['run_id', 'project_name','timestamp', 'duration', 'emissions',
       'emissions_rate', 'cpu_power', 'gpu_power', 'ram_power', 'cpu_energy',
       'gpu_energy', 'ram_energy', 'energy_consumed', 'country_name',
       'country_iso_code', 'region', 'cloud_provider', 'cloud_region', 'os',
       'python_version', 'codecarbon_version', 'cpu_count', 'cpu_model',
       'gpu_count', 'gpu_model', 'ram_total_size',
       'tracking_mode', 'on_cloud', 'longitude', 'latitude']]

    data.columns = ['task_hash','task_name','start_time', 'duration', 'emissions',
       'emissions_rate', 'cpu_power', 'gpu_power', 'ram_power', 'cpu_energy',
       'gpu_energy', 'ram_energy', 'energy_consumed', 'country_name',
       'country_iso_code', 'region', 'cloud_provider', 'cloud_region', 'os',
       'python_version', 'codecarbon_version', 'cpu_count', 'cpu_model',
       'gpu_count', 'gpu_model', 'ram_total_size',
       'tracking_mode', 'on_cloud', 'longitude', 'latitude']
    
    data['postal_code'] = postal_code
    data['task_hash'] = process_id
    data['task_name'] = task_name
    return data


def get_configuration(experiment_name:str=None)-> dict:
    """utility function to load the configuration with the specified name. If no configuration with the specified
    name is found then the default configuration will be used.

    :param experiment_name: _description_, defaults to None
    :type experiment_name: _type_, optional
    :raises ConfigNotFoundException: raise when the requested Configuration is faulty.
    :return: The dictionary containing the parameters specified in the configuration file.
    :rtype: dict
    """

    CONFIG_NUMERIC = ['allowed_delay_hours', 'estimated_runtime_minutes', 'estimated_runtime_hours',
                      'percent_renewable']


    if experiment_name is None:
        p = Path.cwd().resolve() / ".codegreen.config"
    else:
        p = Path.cwd().resolve() / f".{experiment_name}.codegreen.config"
    if p.exists():
        print(p)
        config = configparser.ConfigParser()
        config.read(str(p))
        if "codegreen" in config.sections():
            d = dict(config["codegreen"])
            if 'api_key' not in d.keys():
                raise ConfigNotFoundException('You must specify at least the API Key in an environment file called .codegreen.config')
            if 'api_endpoint' not in d.keys():
                raise ConfigNotFoundException('You must specify at least the API url in an environment file called .codegreen.config')
            for key in CONFIG_NUMERIC:
                if key in d.keys():
                    d[key] = float(d[key])
            if 'area_code' in d:
                d['area_code'] = d['area_code'].split(';')
            return d
    else:
        try:
            return get_configuration()
        except ConfigNotFoundException:
            raise ConfigNotFoundException('You must specify at least the API Key in an environment file called .codegreen.config'+ str(p))

def write_config_file(experiment_name:str, 
                      codecarbon_logfile:str, 
                      nextflow_logfile:str,
                      area_code:list[str], 
                      estimated_runtime_hours:str =2,
                      estimated_runtime_minutes:str= 30, 
                      percent_renewable:int = 30,
                      allowed_delay_hours:int = 24,
                    log_request:bool=True,
                    overwrite:bool=False):
    """Write a configuration file

    :param experiment_name: Name of the experiment for the configuration file
    :type experiment_name: str
    :param codecarbon_logfile: Name of the codecarbon logfile
    :type codecarbon_logfile: str
    :param nextflow_logfile: Name of the nextflow logfile.
    :type nextflow_logfile: str
    :param area_code: list of area codes as a list of strings.
    :type area_code: list[str]
    :param estimated_runtime_hours: estimated run time in hours, defaults to 2
    :type estimated_runtime_hours: str, optional
    :param estimated_runtime_minutes: estimated additional number of hours run time, defaults to 30
    :type estimated_runtime_minutes: str, optional
    :param percent_renewable:, defaults to 30
    :type percent_renewable: int, optional
    :param allowed_delay_hours: _description_, defaults to 24
    :type allowed_delay_hours: int, optional
    :param log_request: _description_, defaults to True
    :type log_request: bool, optional
    :param overwrite: _description_, defaults to False
    :type overwrite: bool, optional
    :return: _description_
    :rtype: _type_
    """

    config = get_configuration(experiment_name=experiment_name)


    # update relevant fields
    if experiment_name is None:
        config['experiment_name'] = f"experiment_{str(time.now().timestamp())}".format
    else:
        if (op.exists(f".{experiment_name}.codegreen.config") and not overwrite):
            return True
        config['experiment_name'] = experiment_name
    
    if allowed_delay_hours is not None:
        config['allowed_delay_hours'] = allowed_delay_hours
    if codecarbon_logfile is not None:
        config['codecarbon_logfile'] = codecarbon_logfile
    if nextflow_logfile is not None:
        logger.warning("Changing the name of the emission file. Call track_emissions with the correct name")
        config['nextflow_logfile'] = nextflow_logfile

    if area_code is not None:
        config['area_code'] = ';'.join(area_code)
    if estimated_runtime_hours is not None:
        config['estimated_runtime_hours'] = estimated_runtime_hours
    if estimated_runtime_minutes is not None:
        config['estimated_runtime_minutes'] = estimated_runtime_minutes
    if percent_renewable is not None:
        config['percent_renewable'] = percent_renewable
    if log_request is not None:
        config['log_request'] = log_request


    #generate a exeriment hash
    config['experiment_hash'] = uuid4()
    
    conf = configparser.ConfigParser()
    conf['codegreen'] = config
    with open(f".{experiment_name}.codegreen.config", 'w') as configfile:
        conf.write(configfile)

    return True