from codegreen.decorators import init_experiment, time_shift, upload_cc_report
from codecarbon import track_emissions
from codegreen.queries import get_location_prediction, get_data
import numpy as np
from datetime import datetime


# Complete example to timeshift the computation, monitor the energy consumption using codecarbon and then upload the report.
#A. decorate the function
@init_experiment(estimated_runtime_hours=1,estimated_runtime_minutes=30,percent_renewable=40,allowed_delay_hours= 24, area_code=["DE-9"],log_request=True,experiment_name="my_experiment",codecarbon_logfile="experiment.log",nextflow_logfile="nextflow.log",overwrite=True)
@time_shift("my_experiment")
@upload_cc_report("my_experiment")
@track_emissions(output_file='experiment.log')
def hello_random_matrix_generator():
    for _ in range(1000):
        np.random.random((1000, 1000))
        
    print("Hello")

#B. run the function
hello_random_matrix_generator()

# Download the data you submitted.
data = get_data('codecarbon', False, 'my_experiment')

# Get a location prediction.
pred = get_location_prediction(estimated_runtime_hours = 1, estimated_run_time_in_minutes=12,percent_renewable=40, hard_finish_time = datetime.utcnow().replace(hour=18, minute=0, second=0).timestamp(),area_code = ['DE-79117', 'CY-1', 'CZ-8'] ,log_request = True, process_id = '1', experiment_name='my_experiment')
print(pred.json())