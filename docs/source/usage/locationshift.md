# Locationshift

We are not able to locationshift the computation as easily as we can timeshift. For completeness, we allow users to compute the best country for their computation within a given time frame.

```python
location = get_location_prediction(
    estimated_runtime_hours = 1, 
    estimated_run_time_in_minutes=12,
    percent_renewable=40, 
    hard_finish_time = datetime.utcnow().timestamp(),
    area_code = ['DE-79117', 'CY-1', 'CZ-8'],
    log_request = True, 
    process_id = '1', 
    experiment_name='my_experiment')

prediction = pred.json()
```