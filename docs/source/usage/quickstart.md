# Usage

## tldr;

In your project base directory, add the following configuration file and add your API key:

```.codegreen.config```
``` 
[codegreen]
api_endpoint = https://codegreen.world/api/v1/data
api_key =  super-secret-api-key
```

Initialize the experiment file using your custom parameters, timeshift the computation, upload the report
and track your ressource usage.

```python
@init_experiment(estimated_runtime_hours=1,
                estimated_runtime_minutes=30,percent_renewable=10,allowed_delay_hours=24,area_code="ES-9",log_request=True,experiment_name="my_experiment",codecarbon_logfile="experiment.log",nextflow_logfile="nextflow.log",overwrite=False)
@time_shift("my_experiment")
@upload_cc_report("my_experiment")
@track_emissions(output_file='experiment.log')
def hello_random_matrix_generator():
        for _ in range(1000):
            np.random.random((1000, 1000))
```
or you can write the configuration yourself and load it in the init decorator ():

```.my_experiment.codegreen.config```
```
api_endpoint = https://codegreen.world/api/v1/data
api_key = my-super-secret-api-key
experiment_name = my_experiment
allowed_delay_hours = 24
codecarbon_logfile = experiment.log
nextflow_logfile = nextflow.log
area_code = DE-9
estimated_runtime_hours = 1
estimated_runtime_minutes = 30
percent_renewable = 40
log_request = True
experiment_hash = be0ff372-42d7-4e14-a12c-a9ff915b4a52
```

```python
@init_experiment(experiment_name="my_experiment")
@time_shift("my_experiment")
@upload_cc_report("my_experiment")
@track_emissions(output_file='experiment.log')
def hello_random_matrix_generator():
    for _ in range(1000):
        np.random.random((1000, 1000))
        
    print("Hello")

hello_random_matrix_generator()
```

## Prerequisites
You have requested an API key for your project. This API key has been sent to you via mail and
is also available through the web interface. You can add multiple API keys for your project and
scope your reporting in a more fine grained manner.

In your project base directory, add the following configuration file: If you are not hosting your own
API in your private domain, leave the API endpoint as is and just modify the api key configuration.
You can also use this configuration file to configure your project parameters. (see below)

```.codegreen.config```
``` 
[codegreen]
api_endpoint = https://codegreen.world/api/v1/data
api_key =  super-secret-api-key
```
## Decorators
The easiest way to timeshift your computation is to add the decorator to your code.

Let's say you want to do a lengthy computation like a simulation or training of a neural network.
You main training loop needs to be implemented in a function that can be decorated.


```python
def hello_random_matrix_generator():
        for _ in range(1000):
            np.random.random((1000, 1000))
```

To time shift the computation, you need to initialize the experiment using the ```@init_experiment``` decorator. You can specify the arguments on the fly, but you can also add them to the ```.my_experiment.codegreen.config``` file. If you set override to true, any parameter you specify will be overridden.   The name of the experiment allows you to match your predictions with your reports. This allows us to compute how much carbon you have saved by using the service :) 

```python
@init_experiment(estimated_runtime_hours=1,estimated_runtime_minutes=30,percent_renewable=10,allowed_delay_hours=24,area_code="ES-9",log_request=True,experiment_name="my_experiment",codecarbon_logfile="experiment.log",nextflow_logfile="nextflow.log",overwrite=False)
def hello_random_matrix_generator():
        for _ in range(1000):
            np.random.random((1000, 1000))
```

Calling the @init_experiment decorator with ```experiment_name="my_experiment"``` will create a new .my_experiment.codegreen.config file with the name of your experiment. You can also directly create your own codecarbon config file. Just make sure that the file name is the one you use later on. (We decided to use a config file to avoid weird scoping issues when nesting decorators.) The content of the config file looks like this:


```
[codegreen]
api_endpoint = https://codegreen.world/api/v1/data
api_key = my-super-secret-api-key
experiment_name = my_experiment
allowed_delay_hours = 24
codecarbon_logfile = experiment.log
nextflow_logfile = nextflow.log
area_code = DE-9
estimated_runtime_hours = 1
estimated_runtime_minutes = 30
percent_renewable = 40
log_request = True
experiment_hash = be0ff372-42d7-4e14-a12c-a9ff915b4a52
```

Next, you can timeshift your experiment, by adding the @timeshift parameter to the function. Make sure that
the name of the experiment is the same as the one specified in the @init_experiment call. This will put your experiment to sleep until the energy is greener. You can now call it a day and wait for your results.

```python
@init_experiment(estimated_runtime_hours=1,estimated_runtime_minutes=30,percent_renewable=10,allowed_delay_hours=24,area_code="ES-9",log_request=True,experiment_name="my_experiment",codecarbon_logfile="experiment.log",nextflow_logfile="nextflow.log",overwrite=False)
@time_shift("my_experiment")
def hello_random_matrix_generator():
        for _ in range(1000):
            np.random.random((1000, 1000))
```

We would love for you to report your usage to the API. Anything that you report will remain private in the sense that only you can access it in the web interface. However, we would like to use the data to improve our 
service and will therefore aggregate the results and compute some statistics to gain an understanding of the energy saving potential of the service.

If you are interested in tracking and reporting your usage, you can use the following two decorators.
```@upload_report``` and ```@track_emissions```. ```@track_emissions``` is a decorator from the codecarbon python package which we reused. Codecarbon also allows uploading the usage, but the functionality did not fulfill our privacy requirements. Furthermore, we are interested in collecting more and different data specifically about bioinformatics usage as well.  

> **Warning**
> Make sure the name of the experiment is specified and the same for all decorators belonging to one function.

```python
@init_experiment(estimated_runtime_hours=1,estimated_runtime_minutes=30,percent_renewable=10,allowed_delay_hours=24,area_code="ES-9",log_request=True,experiment_name="my_experiment",codecarbon_logfile="experiment.log",nextflow_logfile="nextflow.log",overwrite=False)
@time_shift("my_experiment")
@upload_cc_report("my_experiment")
@track_emissions(output_file='experiment.log')
def hello_random_matrix_generator():
        for _ in range(1000):
            np.random.random((1000, 1000))
```

