#Adapted from the codecarbon project

import configparser
from pathlib import Path
from codegreen.logger import logger
from codegreen.expections import ConfigNotFoundException, AreaCodeMisconfiguredException
import os.path as op
from uuid import uuid4
import time

def get_api_endpoint(myexperiment:str = None)->str:
    """ Utility code to load the API enpoint from the configuration file.

    :return: The API url
    :rtype: str
    """
    if myexperiment is not None and myexperiment != "":
        p = Path.cwd().resolve() / f".{myexperiment}.codegreen.config".format()
    else:
        p = Path.cwd().resolve() / ".codegreen.config"
    if p.exists():
        config = configparser.ConfigParser()
        config.read(str(p))
        if "codegreen" in config.sections():
            d = dict(config["codegreen"])
            if "api_endpoint" in d:
                return d["api_endpoint"]+'/'
    return "https://codegreen.world/api/v1/data/"

def get_api_key(myexperiment:str = None)-> str:
    """Get the API key from the configuration file.

    :param myexperiment: name of the experiment to load the API key from, defaults to None
    :type myexperiment: str, optional
    :return: The API key to authenticate with the API
    :rtype: str
    """
    if myexperiment is not None and myexperiment != "":
        p = Path.cwd().resolve() / f".{myexperiment}.codegreen.config".format()
    else:
        p = Path.cwd().resolve() / ".codegreen.config"
    if p.exists():
        config = configparser.ConfigParser()
        config.read(str(p))
        if "codegreen" in config.sections():
            d = dict(config["codegreen"])
            if "api_key" in d:
                return d["api_key"]
    return ""



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

    if experiment_name is None or experiment_name == "":
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
        if type(area_code) == str:
            config['area_code'] = area_code
        elif type(area_code) == list:
            config['area_code'] = ';'.join(area_code)
        else:
            raise AreaCodeMisconfiguredException
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