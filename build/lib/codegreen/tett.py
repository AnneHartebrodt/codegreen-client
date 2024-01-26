from codegreen.decorators import init_experiment, time_shift, upload_cc_report
from codecarbon import track_emissions
from codegreen.queries import get_location_prediction, get_data, submit_nf_resource_usage
from datetime import datetime
from urllib.parse import urljoin

import pandas as pd
import requests

from codegreen.config import get_api_endpoint, get_api_key
from codegreen.expections import (InternalServerErrorException,
                                  UnauthorizedException)
from codegreen.utils import process_codecarbon_file

import numpy as np
from datetime import datetime
payload = {"estimated_runtime_hours": 1,
           "estimated_runtime_minutes": 20,
           "percent_renewable": 20,
           "hard_finish_time": "2023-12-14 07:00",
           "area_code": ["DE"],
           "log_request": True,
           "process_id": "process_id"}

API_URL = get_api_endpoint('my_experiment')
API_KEY = get_api_key('my_experiment')
AUTHORIZATION_HEADER = {'Authorization': f'Bearer {API_KEY}', 'content-type': 'application/json'}
r = requests.post(urljoin(API_URL, 'forecast/timeshift'), json=payload, headers=AUTHORIZATION_HEADER)

get_pred