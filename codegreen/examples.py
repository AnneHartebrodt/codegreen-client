from codegreen.decorators import init_experiment, time_shift, upload_cc_report
from codecarbon import track_emissions
from codegreen.queries import get_location_prediction, get_data, submit_nf_resource_usage

import numpy as np
from datetime import datetime
# Get a location prediction.
location = get_location_prediction(estimated_runtime_hours = 1,
                               estimated_run_time_in_minutes=12,
                               percent_renewable=40,
                               hard_finish_time = datetime.utcnow().replace(hour=23, minute=0, second=0).timestamp(),
                               area_code = ['DE-79117', 'CY-1', 'CZ-8'],
                               log_request = True,
                               process_id = '1',
                               experiment_name='my_experiment')
@init_experiment(experiment_name="my_local_experiment")
@time_shift("my_local_experiment")
@upload_cc_report("my_local_experiment")
@track_emissions(output_file='my_local_experiment.log')
def hello_random_matrix_generator():
    for _ in range(1000):
        np.random.random((1000, 1000))
        
    print("Hello")

#B. run the function
hello_random_matrix_generator()

@init_experiment(experiment_name="my_experiment")
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



@init_experiment(experiment_name="my_local_experiment")

submit_nf_resource_usage('/home/bionets-og86asub/Documents/greenerai/greenerai-client/nf-module/trace-20230614-65123194.txt', process_id='nextflow', experiment_name='my_local_experiment')





