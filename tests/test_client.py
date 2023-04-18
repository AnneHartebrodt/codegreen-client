from client import get_prediction
from datetime import datetime, timedelta, timezone

AUTHORIZATION_HEADER = {'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2ODAwOTcwMTIsInN1YiI6IjMxOThmMjVlLWRhNWEtNDI3ZC1iMDQwLWJlNDM4MDA1YzQ1NSJ9.rWR75a__ArEqeD28AorSLsOXHzO_iXVbjCrnzH2eBb4'}


def test_valid_prediction():
    valid_requests = generate_valid_requests()
    for vp in valid_requests:
        response = get_prediction(vp['estimated_runtime_hours'],
                       vp['estimated_runtime_minutes'],
                       vp['percent_renewable'],
                       vp['hard_finish_time'])
    # write assertions

def test_invalid_prediction():
    invalid_requests = generate_invalid_requests()
    for vp in invalid_requests:
        response = get_prediction(vp['estimated_runtime_hours'],
                       vp['estimated_runtime_minutes'],
                       vp['percent_renewable'],
                       vp['hard_finish_time'])
    # write assertions

def generate_valid_requests():
    """
    Generate a list of payloads to test 
    """

    payload_list  = []
    # the expected run time ranging between 0 and 24
    for rh in range(0, 24, 6):
        # the expected run time in minutes
        for rm in range(0, 60, 20):
            # The expected percentage of renewables (allow 0.1 and 10 as percentages)
            for pr in range(0, 1, 0.1):
                # Finishdate computed as rh+offset transformed into a date.
                # Offset will be at a constant 5 hours leeway.
                hard_finish_time = datetime.now()+timedelta(hours = rh+5)
                payload = {'estimated_runtime_hours': rh, 
                            'estimated_runtime_minutes': rm,
                            'percent_renewable': pr,
                            'hard_finish_time': hard_finish_time.strftime('%Y-%m-%d %H:%M')  }
                payload_list.append(payload)
    return payload_list
                
def generate_invalid_requests():

    """
    For now all these request should have a default message and return the 
    current time as the correct time.

    """

    payload_list = []
    # negative hour not allowed.
    hard_finish_time = datetime.now(timezone.utc)+timedelta(hours=5)
    payload = {'estimated_runtime_hours': -1, 
                'estimated_runtime_minutes': 20,
                'percent_renewable': 0.3,
                'hard_finish_time': hard_finish_time.strftime('%Y-%m-%d %H:%M')  }
    payload_list.append(payload)

    # negative minutes not allowed
    hard_finish_time = datetime.now(timezone.utc)+timedelta(hours=5)
    payload = {'estimated_runtime_hours': 1, 
                            'estimated_runtime_minutes': -21,
                            'percent_renewable': 0.3,
                            'hard_finish_time': hard_finish_time.strftime('%Y-%m-%d %H:%M')  }
    payload_list.append(payload)

    # minutes above 59 not allowed
    hard_finish_time = datetime.now(timezone.utc)+timedelta(hours=10)
    payload = {'estimated_runtime_hours': 1, 
                            'estimated_runtime_minutes': 242,
                            'percent_renewable': 0.3,
                            'hard_finish_time': hard_finish_time.strftime('%Y-%m-%d %H:%M')  }
    payload_list.append(payload)
    
    # percentage over 100 not allowed
    hard_finish_time = datetime.now(timezone.utc)+timedelta(hours=5)
    payload = {'estimated_runtime_hours': 1, 
                            'estimated_runtime_minutes': 20,
                            'percent_renewable': 110,
                            'hard_finish_time': hard_finish_time.strftime('%Y-%m-%d %H:%M')  }
    payload_list.append(payload)

    # percentage below 0 not allowed
    hard_finish_time = datetime.now(timezone.utc)+timedelta(hours=5)
    payload = {'estimated_runtime_hours': 1, 
                            'estimated_runtime_minutes': 12,
                            'percent_renewable': -93,
                            'hard_finish_time': hard_finish_time.strftime('%Y-%m-%d %H:%M')  }
    payload_list.append(payload)

    # finish times in the past are not allowed
    hard_finish_time = datetime.now(timezone.utc)+timedelta(hours=-1)
    payload = {'estimated_runtime_hours': 1, 
                            'estimated_runtime_minutes': 12,
                            'percent_renewable': 0.3,
                            'hard_finish_time': hard_finish_time.strftime('%Y-%m-%d %H:%M')}
    payload_list.append(payload)

    return payload_list

    

