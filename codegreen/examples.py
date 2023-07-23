from codegreen.decorators import init_experiment, time_shift, upload_cc_report

from codecarbon import track_emissions
from codegreen.queries import get_location_prediction, get_data
import numpy as np
from datetime import datetime


# Complete example to timeshift the computation, monitor the energy consumption using codecarbon and then upload the report.
#A. decorate the function
#@init_experiment(estimated_runtime_hours=1,estimated_runtime_minutes=30,percent_renewable=40,allowed_delay_hours= 24, area_code=["DE-9"],log_request=True,experiment_name="my_experiment",codecarbon_logfile="experiment.log",nextflow_logfile="nextflow.log",overwrite=True)

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


# Get a location prediction.
location = get_location_prediction(estimated_runtime_hours = 1, 
                               estimated_run_time_in_minutes=12,
                               percent_renewable=40, 
                               hard_finish_time = datetime.utcnow().replace(hour=18, minute=0, second=0).timestamp(),
                               area_code = ['DE-79117', 'CY-1', 'CZ-8'],
                               log_request = True, 
                               process_id = '1', 
                               experiment_name='my_experiment')


from entsoe import EntsoePandasClient
import pandas as pd



start = pd.Timestamp('20230720', tz='UTC')
end = pd.Timestamp('20230721', tz='UTC')
country_code = 'DE'
print(start)
print(end)
print(country_code)
entsoe_client = EntsoePandasClient(api_key= "3dd18ef6-867a-4b4e-9930-022893ebd580")
gen_for = entsoe_client.query_generation_forecast(
    country_code, start=start, end=end
)
gen_for = pd.DataFrame(gen_for)
gen_for = gen_for.rename(columns={"Actual Aggregated": "total_energy"})
print(gen_for)
gen_sw_for = entsoe_client.query_wind_and_solar_forecast(
    country_code, start=start, end=end, psr_type=None
)
gen_sw_for = gen_sw_for.rename(
    columns={
        "Solar": "solar",
        "Wind Onshore": "wind_onshore",
        "Wind Offshore": "wind_offshore",
    }
)

gen_sw_for["total_renewable"] = gen_sw_for.sum(axis=1)
print(gen_sw_for)
gen_for = gen_for.merge(gen_sw_for, left_index=True, right_index=True)

timeinterval = pd.Timedelta(
    gen_for.index[1] - gen_for.index[0]
).components.minutes + (
    60 * pd.Timedelta(gen_for.index[1] - gen_for.index[0]).components.hours
)

gen_for["percent_renewable"] = (
    (gen_for["total_renewable"] / gen_for["total_energy"])* 100* (timeinterval / 60)
)

gen_for["startTime"] = gen_for.index
gen_for["posix_timestamp"] = (gen_for["startTime"] - pd.Timestamp("1970-01-01",  tz='UTC') ) // pd.Timedelta('1s')
gen_for['e']
