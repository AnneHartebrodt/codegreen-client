import requests
import logging
import random
import os
from datetime import datetime, timedelta
import time
import json

API_URL = "http://localhost:5000/api/v1/data/forecast/locationshift"
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MDI1NTczNjQsInN1YiI6IjI0OWE3OGJhLTI5NjYtNGIxZi04NjhjLTk3ZDA5M2I2OWUxOCIsInNjb3BlIjoiYXNkZlNBRCJ9.E0-JjG-tTwHKJtfPgsWixynvv6NQjKnnJkfibBmdWMY"
SLEEP_DURATION = 5  # Duration to sleep between requests, in seconds


def setup_logger(country_code='locationshift'):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Define log file path in 'logs/api_logs' subdirectory
    log_directory = os.path.join(project_root, 'logs', 'api_timeshit_logs')
    os.makedirs(log_directory, exist_ok=True)

    log_filename = os.path.join(log_directory, f'{country_code.lower()}_api_test.log')

    # Setup logger
    logger = logging.getLogger(country_code)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        file_handler = logging.FileHandler(log_filename)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Hard Finish Time Calculation
def get_hard_finish_time(additional_time):
    return (datetime.utcnow() + additional_time).timestamp()


# Test Body Creation
def create_test_body(percent_renewable, hours, minutes, area_codes, hard_time):
    # if not isinstance(area_codes, list) or not all(isinstance(code, tuple) for code in area_codes):
    #     raise ValueError("area_codes must be a list of tuples")

    return {
        "estimated_runtime_hours": hours,
        "estimated_runtime_minutes": minutes,
        "percent_renewable": percent_renewable,
        "area_code": area_codes,
        "process_id": "1",
        "log_request": False,
        "hard_finish_time": hard_time
    }


# Random Area Code Selection
def get_random_area_codes(countries_and_cities, num_per_country=4):
    area_codes = {}
    for country, cities in countries_and_cities.items():
        selected_cities = random.sample(cities, min(len(cities), num_per_country))
        for city in selected_cities:
            for key, value in city.items():
                if country in area_codes:
                    area_codes[country].append(value)
                else:
                    area_codes[country] = [value]
    return area_codes


# Test Execution
def run_tests():
    countries_and_cities = {
        'DE': [
            {"Berlin": "10115"},
            {"Hamburg": "20095"},
            {"Munich": "80331"},
            {"Cologne": "50667"},
            {"Frankfurt": "60311"},
            {"Stuttgart": "70173"},
            {"Düsseldorf": "40210"},
            {"Dortmund": "44135"},
            {"Essen": "45127"},
            {"Leipzig": "04109"}],
        'BE': [
            {"Brussels": "1000"},
            {"Antwerp": "2000"},
            {"Ghent": "9000"},
            {"Charleroi": "6000"},
            {"Liège": "4000"},
            {"Bruges": "8000"},
            {"Namur": "5000"},
            {"Leuven": "3000"},
            {"Mons": "7000"},
            {"Aalst": "9300"}
        ],
        'BG': [
            {"Sofia": "1000"},
            {"Plovdiv": "4000"},
            {"Varna": "9000"},
            {"Burgas": "8000"},
            {"Ruse": "7000"},
            {"Stara Zagora": "6000"},
            {"Pleven": "5800"},
            {"Sliven": "8800"},
            {"Dobrich": "9300"},
            {"Shumen": "9700"}
        ],
        'HR': [
            {"Zagreb": "10000"},
            {"Split": "21000"},
            {"Rijeka": "51000"},
            {"Osijek": "31000"},
            {"Zadar": "23000"},
            {"Slavonski Brod": "35000"},
            {"Pula": "52100"},
            {"Sesvete": "10360"},
            {"Karlovac": "47000"},
            {"Varaždin": "42000"}
        ],
        'CY': [
            {"Nicosia": "1010"},
            {"Limassol": "3105"},
            {"Larnaca": "6015"},
            {"Paphos": "8010"},
            {"Famagusta": "5280"},
            {"Kyrenia": "99300"},
            {"Protaras": "5296"},
            {"Morphou": "9970"},
            {"Aradippou": "7101"},
            {"Paralimni": "5288"}
        ],
        'CZ': [
            {"Prague": "110 00"},
            {"Brno": "602 00"},
            {"Ostrava": "702 00"},
            {"Plzeň": "301 00"},
            {"Liberec": "460 01"},
            {"Olomouc": "779 00"},
            {"Ústí nad Labem": "400 01"},
            {"Hradec Králové": "500 03"},
            {"České Budějovice": "370 01"},
            {"Pardubice": "530 02"}
        ],
        'DK': [
            {"Copenhagen": "1000"},
            {"Aarhus": "8000"},
            {"Odense": "5000"},
            {"Aalborg": "9000"},
            {"Esbjerg": "6700"},
            {"Randers": "8900"},
            {"Kolding": "6000"},
            {"Horsens": "8700"},
            {"Vejle": "7100"},
            {"Roskilde": "4000"}
        ],
        'EE': [
            {"Tallinn": "10111"},
            {"Tartu": "51003"},
            {"Narva": "20307"},
            {"Pärnu": "80010"},
            {"Kohtla-Järve": "30328"},
            {"Viljandi": "71020"},
            {"Rakvere": "44310"},
            {"Maardu": "74115"},
            {"Kuressaare": "93815"},
            {"Võru": "65609"}
        ],
        'FI': [
            {"Helsinki": "00100"},
            {"Espoo": "02100"},
            {"Tampere": "33100"},
            {"Vantaa": "01300"},
            {"Turku": "20100"},
            {"Oulu": "90100"},
            {"Lahti": "15110"},
            {"Kuopio": "70100"},
            {"Jyväskylä": "40100"},
            {"Pori": "28100"}
        ],
        'FR': [
            {"Paris": "75001"},
            {"Marseille": "13001"},
            {"Lyon": "69001"},
            {"Toulouse": "31000"},
            {"Nice": "06000"},
            {"Nantes": "44000"},
            {"Strasbourg": "67000"},
            {"Montpellier": "34000"},
            {"Bordeaux": "33000"},
            {"Lille": "59000"}
        ],
        'AT': [
            {"Vienna": "1010"},
            {"Graz": "8010"},
            {"Linz": "4020"},
            {"Salzburg": "5020"},
            {"Innsbruck": "6020"},
            {"Klagenfurt": "9020"},
            {"Villach": "9500"},
            {"Wels": "4600"},
            {"Sankt Pölten": "3100"},
            {"Dornbirn": "6850"}
        ],
        'GR': [
            {"Athens": "1050"},
            {"Thessaloniki": "54621"},
            {"Patras": "26221"},
            {"Heraklion": "71201"},
            {"Larissa": "41221"},
            {"Volos": "38221"},
            {"Ioannina": "45221"},
            {"Trikala": "42100"},
            {"Chania": "73100"},
            {"Kavala": "65403"}
        ],
        'HU': [
            {"Budapest": "1011"},
            {"Debrecen": "4024"},
            {"Szeged": "6720"},
            {"Miskolc": "3525"},
            {"Pécs": "7621"},
            {"Győr": "9021"},
            {"Nyíregyháza": "4400"},
            {"Kecskemét": "6000"},
            {"Székesfehérvár": "8000"},
            {"Szombathely": "9700"}
        ],
        'IE': [
            {"Dublin": "D01"},
            {"Cork": "T12"},
            {"Limerick": "V94"},
            {"Galway": "H91"},
            {"Waterford": "X91"},
            {"Drogheda": "A92"},
            {"Dundalk": "A91"},
            {"Bray": "A98"},
            {"Navan": "C15"},
            {"Ennis": "V95"}
        ],
        'IT': [
            {"Rome": "00118"},
            {"Milan": "20121"},
            {"Naples": "80121"},
            {"Turin": "10121"},
            {"Palermo": "90121"},
            {"Genoa": "16121"},
            {"Bologna": "40121"},
            {"Florence": "50121"},
            {"Bari": "70121"},
            {"Catania": "95121"}
        ],
        'LV': [
            {"Riga": "LV-1010"},
            {"Daugavpils": "LV-5401"},
            {"Liepāja": "LV-3401"},
            {"Jelgava": "LV-3001"},
            {"Jūrmala": "LV-2010"},
            {"Ventspils": "LV-3601"},
            {"Rēzekne": "LV-4601"},
            {"Valmiera": "LV-4201"},
            {"Jēkabpils": "LV-5201"},
            {"Ogre": "LV-5001"}
        ],
        'LT': [
            {"Vilnius": "01101"},
            {"Kaunas": "44001"},
            {"Klaipėda": "92101"},
            {"Šiauliai": "76001"},
            {"Panevėžys": "35101"},
            {"Alytus": "62101"},
            {"Marijampolė": "68101"},
            {"Mažeikiai": "89201"},
            {"Jonava": "55101"},
            {"Utena": "28101"}
        ],
        'LU': [
            {"Luxembourg City": "L-1009"},
            {"Esch-sur-Alzette": "L-4010"},
            {"Differdange": "L-4501"},
            {"Dudelange": "L-3401"},
            {"Ettelbruck": "L-9001"},
            {"Diekirch": "L-9201"},
            {"Wiltz": "L-9501"},
            {"Echternach": "L-6401"},
            {"Rumelange": "L-3701"},
            {"Grevenmacher": "L-6701"}
        ],
        'MT': [
            {"Valletta": "VLT 1000"},
            {"Mdina": "MDN 1000"},
            {"Birkirkara": "BKR 1000"},
            {"Qormi": "QRM 1000"},
            {"Mosta": "MST 1000"},
            {"Żabbar": "ZBR 1000"},
            {"Sliema": "SLM 1000"},
            {"Żebbuġ": "ZBG 1000"},
            {"Fgura": "FGR 1000"},
            {"Żejtun": "ZTN 1000"}
        ],
        'NL': [
            {"Amsterdam": "1011"},
            {"Rotterdam": "3011"},
            {"The Hague": "2511"},
            {"Utrecht": "3511"},
            {"Eindhoven": "5611"},
            {"Tilburg": "5011"},
            {"Groningen": "9711"},
            {"Almere": "1311"},
            {"Breda": "4811"},
            {"Nijmegen": "6511"}
        ],
        'PL': [
            {"Warsaw": "00-001"},
            {"Kraków": "30-001"},
            {"Łódź": "90-001"},
            {"Wrocław": "50-001"},
            {"Poznań": "60-001"},
            {"Gdańsk": "80-001"},
            {"Szczecin": "70-001"},
            {"Bydgoszcz": "85-001"},
            {"Lublin": "20-001"},
            {"Katowice": "40-001"}
        ],
        'PT': [
            {"Lisbon": "1000-001"},
            {"Porto": "4000-001"},
            {"Vila Nova de Gaia": "4400-001"},
            {"Amadora": "2700-001"},
            {"Braga": "4700-001"},
            {"Funchal": "9000-001"},
            {"Coimbra": "3000-001"},
            {"Queluz": "2745-001"},
            {"Almada": "2800-001"},
            {"Setúbal": "2900-001"}
        ],
        'RO': [
            {"Bucharest": "010011"},
            {"Cluj-Napoca": "400001"},
            {"Timișoara": "300001"},
            {"Iași": "700001"},
            {"Constanța": "900001"},
            {"Craiova": "200001"},
            {"Brașov": "500001"},
            {"Galați": "800001"},
            {"Ploiești": "100001"},
            {"Oradea": "410001"}
        ],
        'SK': [
            {"Bratislava": "811 01"},
            {"Košice": "040 01"},
            {"Prešov": "080 01"},
            {"Žilina": "010 01"},
            {"Nitra": "949 01"},
            {"Banská Bystrica": "974 01"},
            {"Trnava": "917 01"},
            {"Martin": "036 01"},
            {"Trenčín": "911 01"},
            {"Poprad": "058 01"}
        ],
        'SI': [
            {"Ljubljana": "1000"},
            {"Maribor": "2000"},
            {"Celje": "3000"},
            {"Kranj": "4000"},
            {"Velenje": "3320"},
            {"Koper": "6000"},
            {"Novo Mesto": "8000"},
            {"Ptuj": "2250"},
            {"Trbovlje": "1420"},
            {"Kamnik": "1241"}
        ],
        'ES': [
            {"Madrid": "28001"},
            {"Barcelona": "08001"},
            {"Valencia": "46001"},
            {"Seville": "41001"},
            {"Zaragoza": "50001"},
            {"Málaga": "29001"},
            {"Murcia": "30001"},
            {"Palma": "07001"},
            {"Las Palmas": "35001"},
            {"Bilbao": "48001"}
        ],
        'SE': [
            {"Stockholm": "111 64"},
            {"Gothenburg": "411 02"},
            {"Malmö": "211 39"},
            {"Uppsala": "753 20"},
            {"Västerås": "721 87"},
            {"Örebro": "701 82"},
            {"Linköping": "581 83"},
            {"Helsingborg": "252 78"},
            {"Jönköping": "551 11"},
            {"Norrköping": "601 81"}
        ],
        'CH': [
            {"Zurich": "8001"},
            {"Geneva": "1201"},
            {"Basel": "4001"},
            {"Lausanne": "1003"},
            {"Bern": "3001"},
            {"Winterthur": "8400"},
            {"Lucerne": "6003"},
            {"St. Gallen": "9000"},
            {"Lugano": "6900"},
            {"Biel/Bienne": "2502"}
        ]
    }

    test_cases = [
        # Typical scenarios
        (30, 0, 45, timedelta(minutes=15), "Average renewable energy, under 1 hour, short-term future"),
        (70, 1, 15, timedelta(hours=2), "High renewable energy, slightly over 1 hour, near-term future"),
        (10, 2, 0, timedelta(hours=4), "Low renewable energy, 2 hours runtime, medium-term future"),

        # Boundary conditions
        (0, 0, 1, timedelta(minutes=5), "Zero percent renewable, minimal runtime, very short-term future"),
        (100, 0, 0, timedelta(minutes=0), "Full renewable energy, zero runtime, immediate request"),

        # Long-term future
        (80, 5, 30, timedelta(days=1), "High renewable energy, long runtime, long-term future"),

        # Edge cases
        (50, 0, 0, timedelta(minutes=-10), "Runtime with negative time delta (should fail)"),
        (50, 23, 59, timedelta(hours=24), "Maximum possible runtime within a day"),

        # Invalid inputs
        (-1, 1, 30, timedelta(hours=1), "Negative percent renewable (invalid input)"),
        (101, 0, 30, timedelta(minutes=30), "Percent renewable more than 100 (invalid input)"),
        (50, -1, 0, timedelta(hours=1), "Negative runtime hours (invalid input)"),
        (50, 1, -1, timedelta(hours=1), "Negative runtime minutes (invalid input)"),
        (50, 1, 60, timedelta(hours=1), "Runtime minutes equal to 60 (invalid input)"),

        # Special cases
        (50, 24, 0, timedelta(hours=48), "24 hours runtime, 2 days into the future"),
        (50, 0, 0, timedelta(weeks=1), "Zero runtime, 1 week into the future (schedule check)"),

        # # Postcode and country combinations
        # (50, 1, 30, timedelta(hours=1), "Valid runtime with multiple country-postcode combinations"),
        #
        # # Example test case with multiple country-postcode combinations
        # (50, 1, 30, timedelta(hours=1), "Valid runtime with multiple country-postcode combinations",
        #  [('DE', '10115'), ('BE', '1000')]),
    ]

    headers = {'Authorization': f"Bearer {JWT_TOKEN}", 'content-type': 'application/json'}

    for test_case in test_cases:
        percent_renewable, hours, minutes, time_delta, description = test_case
        area_codes = get_random_area_codes(countries_and_cities, num_per_country=1)
        areacode_list = [f"{country}-{code}" for country, postalcodes in area_codes.items() for code in postalcodes]

        body = create_test_body(percent_renewable, hours, minutes, areacode_list, get_hard_finish_time(time_delta))

        logger = setup_logger()

        logger.info(f"Running test case: {description}")
        response = requests.post(API_URL, json=body, headers=headers)
        logger.info(f"Request: {json.dumps(body, indent=2)}")

        try:
            json_data = response.json()
            logger.info(f"Response JSON: {json.dumps(json_data, indent=2)}")
        except ValueError:
            print("Response is not JSON")
            response_text_lines = response.text.splitlines()
            preview = response_text_lines[:3]
            logger.info(f"{response.status_code}, Response (not JSON, first few lines): {' '.join(preview)}")



if __name__ == "__main__":
    run_tests()
    print("Testing completed")