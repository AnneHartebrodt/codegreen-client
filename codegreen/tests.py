import unittest
import logging
import time
from datetime import datetime, timedelta
import requests
from enum import Enum

class Message(Enum):
    OPTIMAL_TIME = 'OPTIMAL_TIME'
    NO_DATA = 'NO_DATA'
    RUNTIME_LONGER_THAN_DEADLINE_ALLOWS = 'RUNTIME_LONGER_THAN_DEADLINE_ALLOWS'
    

API_URL = "http://127.0.0.1:5000/api/v1/data/forecast/timeshift"
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2ODk2OTc4MDEsInN1YiI6ImE3NjAyNDJkLTZjMTAtNDdlNy1iNTkxLWNkYjUxYzc5NmY1YyIsInNjb3BlIjoiIn0.btbNWux6Moxz7MbraCznuD5Qzl6pHMfoCIsj7nIUxeY"
SLEEP_DURATION = 5

test_data = [
    (5, 0, 15, timedelta(hours=1), True, [Message.OPTIMAL_TIME.value, Message.NO_DATA.value]),
    
    
    (50, 1, 30, timedelta(hours=1), False, [Message.RUNTIME_LONGER_THAN_DEADLINE_ALLOWS.value, Message.NO_DATA.value]),
    (50, 1, 30, timedelta(hours=1), False, [Message.RUNTIME_LONGER_THAN_DEADLINE_ALLOWS.value, Message.NO_DATA.value]),

    # Add more test data tuples...
]

# Iterate over all possible percentage values. negative > 0, greater 100 > 100.
for i in range(-10,120, 10):
    test_data.append((i, 1, 30, timedelta(hours=1), False, [Message.RUNTIME_LONGER_THAN_DEADLINE_ALLOWS.value, Message.NO_DATA.value]))
    test_data.append((i, 0, 30, timedelta(minutes = 15), False, [Message.RUNTIME_LONGER_THAN_DEADLINE_ALLOWS.value, Message.NO_DATA.value]))
    test_data.append((i, 26, 30, timedelta(hours = 24), False, [Message.RUNTIME_LONGER_THAN_DEADLINE_ALLOWS.value, Message.NO_DATA.value]))
    
    
    test_data.append((i, 1, 30, timedelta(hours=2), False, [Message.OPTIMAL_TIME.value, Message.NO_DATA.value]))
    test_data.append((i, 0, 30, timedelta(minutes = 45), False, [Message.OPTIMAL_TIME.value, Message.NO_DATA.value]))
    test_data.append((i, 26, 30, timedelta(hours = 45), False, [Message.OPTIMAL_TIME.value, Message.NO_DATA.value]))


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.countries_to_test = ['DE', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'AT', 'GR', 'HU', 'IE',
                                  'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE', 'CH']
        self.headers = {'Authorization': f'Bearer {JWT_TOKEN}', 'content-type': 'application/json'}

    def get_hard_finish_time(self, additional_time):
        return int((datetime.now() + additional_time).timestamp())

    def create_test_body(self, percent_renewable, hours, minutes, area_code, hard_time, log_request):
        return {
            "estimated_runtime_hours": hours,
            "estimated_runtime_minutes": minutes,
            "percent_renewable": percent_renewable,
            "area_code": area_code,
            "process_id": "1",
            "log_request": log_request,
            "hard_finish_time": hard_time
        }

    def test_api_with_params(self):
        for country in self.countries_to_test:
            for percent_renewable, hours, minutes, time_delta, logging, expected_response in test_data:
                with self.subTest(area_code=country, percent_renewable=percent_renewable, hours=hours,
                                minutes=minutes, time_delta=time_delta):
                    response = self._send_request(country, percent_renewable, hours, minutes, time_delta, logging)
                    self.assertEqual(response.status_code, 200)
                    response_json = response.json()
                    self.assertIn(response_json['message'], expected_response)
            break



    def _send_request(self, area_code, percent_renewable, hours, minutes, time_delta, logging):
        body = {
            "estimated_runtime_hours": hours,
            "estimated_runtime_minutes": minutes,
            "percent_renewable": percent_renewable,
            "area_code": area_code,
            "process_id": "1",
            "log_request": logging,
            "hard_finish_time": int((datetime.now() + time_delta).timestamp())
        }
        return requests.post(API_URL, json=body, headers=self.headers)


    def setup_logger(self, country_code):
        log_filename = f'{country_code.lower()}_api_test.log'
        logger = logging.getLogger(country_code)
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            file_handler = logging.FileHandler(log_filename)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        return logger

    def log_response(self, response, logger):
        try:
            json_data = response.json()
            logger.info(f"Response JSON: {json_data}")
        except ValueError:
            response_text_lines = response.text.splitlines()
            preview = response_text_lines[:3]
            logger.info(f"{response.status_code}, Response (not JSON, first few lines): {' '.join(preview)}")

    

if __name__ == "__main__":
    unittest.main()