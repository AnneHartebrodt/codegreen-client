
import pandas as pd


def process_codecarbon_file(filename, task_hash, task_name, postal_code)-> pd.DataFrame:
    """
    Read file and remove longitude and latitude from file.
    """
    data = pd.read_csv(filename, sep=',', header=0)
    data = data[['timestamp', 'duration', 'emissions',
       'emissions_rate', 'cpu_power', 'gpu_power', 'ram_power', 'cpu_energy',
       'gpu_energy', 'ram_energy', 'energy_consumed', 'country_name',
       'country_iso_code', 'region', 'cloud_provider', 'cloud_region', 'os',
       'python_version', 'codecarbon_version', 'cpu_count', 'cpu_model',
       'gpu_count', 'gpu_model', 'ram_total_size',
       'tracking_mode', 'on_cloud']]

    data.columns = ['start_time', 'duration', 'emissions',
       'emissions_rate', 'cpu_power', 'gpu_power', 'ram_power', 'cpu_energy',
       'gpu_energy', 'ram_energy', 'energy_consumed', 'country_name',
       'country_iso_code', 'region', 'cloud_provider', 'cloud_region', 'os',
       'python_version', 'codecarbon_version', 'cpu_count', 'cpu_model',
       'gpu_count', 'gpu_model', 'ram_total_size',
       'tracking_mode', 'on_cloud']
    data['task_hash'] = task_hash
    data['task_name'] = task_name
    data['postal_code'] = postal_code
    return data

