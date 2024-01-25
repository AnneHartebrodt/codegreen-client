
import pandas as pd
import configparser
from pathlib import Path
import os.path as op
from datetime import datetime, timedelta




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

