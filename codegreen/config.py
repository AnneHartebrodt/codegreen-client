
#Shamelessly copied from the codecarbon project

import configparser
from pathlib import Path


def get_api_endpoint():
    p = Path.cwd().resolve() / ".codegreen.config"
    if p.exists():
        config = configparser.ConfigParser()
        config.read(str(p))
        if "codegreen" in config.sections():
            d = dict(config["codegreen"])
            if "api_endpoint" in d:
                return d["api_endpoint"]
    return "https://api.carbonaware.io"

def get_api_key():
    p = Path.cwd().resolve() / ".codegreen.config"
    if p.exists():
        config = configparser.ConfigParser()
        config.read(str(p))
        if "codegreen" in config.sections():
            d = dict(config["codegreen"])
            if "api_key" in d:
                return d["api_key"]
    return None
