# codegreen python client :seedling:
This repository contains the source code for the codegreen python client. For more information on the usage and background of this tool please go to our documentation on Readthedocs and the website [https://codegreen.world](https://codegreen.world). Please note that in order to use this webservice, you will need to generate an API key on the website.

> **Warning**
> We are extremely happy that you consider using our tool. We are still actively developing the functionalities. If there are problems, please file and issue or contact us directly. Stay green! :seedling:

##
## Functionalities
This package is designed to make timeshifting computations easy. They main functionalities are
1. Providing python decorators to timeshift, monitor and report the carbon footprint of computation. The functionalities can of course also be used indvidually.

2. Provide workflow interfaces (for nextflow, and potential other frameworks, such as Pytorch, etc)
The workflow interfaces should allow the same functionalitities as in 1) but streamlines to work in a copy-paste manner with the workflow manager.

## Installation

We are actively developing the tools, for now you can install the code locally as a pip package.
```
git clone https://github.com/AnneHartebrodt/codegreen-client
cd codegreen
pip install -e .
```
## Usage
### Request an API key
In order to use the API, please generate an API key on the website [https://codegreen.world](https://codegreen.world).  Then you can add a base configuration file to your project. You can have project specific API Keys to facilitate scope reporting.

```.codegreen.config```
```
[codegreen]
api_endpoint = https://codegreen.world/api/v1/data/
api_key =  your-personal-api-key
```

### Decorate a function to timeshift monitor and report
We expect most people to use the decorators. Here is an example of how to decorate a function to timeshift, monitor and report the carbon emission of the computation.
For more verbose and detailed documentation, please follow this link: readthedocs.

```
@init_experiment(estimated_runtime_hours=1,estimated_runtime_minutes=30,percent_renewable=40,allowed_delay_hours= 24, area_code="DE-9",log_request=True,experiment_name="my_experiment",codecarbon_logfile="experiment.log",nextflow_logfile="nextflow.log",overwrite=True)
@time_shift("my_experiment")
@upload_cc_report("my_experiment")
@track_emissions(output_file='experiment.log')
def hello_random_matrix_generator():
    for _ in range(1000):
        np.random.random((1000, 1000))

```
> **Warning**
> The initialization writes a new configuation file which defines the API key, the other parameters, and the name of the experiment. If you want to modify these parameters you have to reinitialize the function!
```
hello_random_matrix_generator()
```

### Get a prediction of the optimal time
Location shifting is more difficult to implement in a generic fashion. We provide an endpoint to return the current best location among a selection of countries and postal codes, but we cannot location shift for you. The paramters are similar to the timeshift parameter.
```
pred = get_location_prediction(estimated_runtime_hours = 1, estimated_run_time_in_minutes=12,percent_renewable=40, hard_finish_time = datetime.utcnow().replace(hour=18, minute=0, second=0).timestamp(),area_code = ['DE-79117', 'CY-1', 'CZ-8'] ,log_request = True, process_id = '1')

```

### Download your data.
You can also download your Request history and you submitted data (for one API key)

```
data = get_data('codecarbon', False)
requests = get_data('requests', False)

```


