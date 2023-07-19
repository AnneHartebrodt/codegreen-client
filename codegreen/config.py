
#Shamelessly copied from the codecarbon project

import configparser
from pathlib import Path


def get_api_endpoint(myexperiment:str = None)->str:
    """ Utility code to load the API enpoint from the configuration file.

    :return: The API url
    :rtype: str
    """
    if myexperiment is not None:
        p = Path.cwd().resolve() / f".{myexperiment}.codegreen.config".format()
    else:
        p = Path.cwd().resolve() / ".codegreen.config"
    if p.exists():
        config = configparser.ConfigParser()
        config.read(str(p))
        if "codegreen" in config.sections():
            d = dict(config["codegreen"])
            if "api_endpoint" in d:
                return d["api_endpoint"]
    return "https://codegreen.world/api/v1"

def get_api_key(myexperiment:str = None)-> str:
    """Get the API key from the configuration file.

    :param myexperiment: name of the experiment to load the API key from, defaults to None
    :type myexperiment: str, optional
    :return: The API key to authenticate with the API
    :rtype: str
    """
    if myexperiment is not None:
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
    return None
