"""Usage: run_boostdiff.py -c FILE -d FILE -o FOLDER

Wrapper script taking as input the case and control files.

-h --help               show this
-s --hours FILE    specify input file
-m --minutes FILE    specify input file
-p --percent_renewable FOLDER      specify output folder
-f --hard_finish_time FOLDER      specify output folder
-c --area_code AREA_CODE format DE-79113 (or fewer digits, at least one)
-a --authorization_header API KEY (keep secret)

--verbose    print more text

"""

from docopt import docopt
import requests
import time
from datetime import timedelta, datetime, timezone
import functools
import pandas as pd


AUTHORIZATION_HEADER = {'Authorization': 
           'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2ODAwOTcwMTIsInN1YiI6IjMxOThmMjVlLWRhNWEtNDI3ZC1iMDQwLWJlNDM4MDA1YzQ1NSJ9.rWR75a__ArEqeD28AorSLsOXHzO_iXVbjCrnzH2eBb4'}

from client import sleep_until

def __main__():
    arguments = docopt(__doc__, version='Boostdiff postprocessing')
    print(arguments)
    sleep_until(arguments['--hours'], arguments['--minutes'], arguments['--percent_renewable'], arguments['--hard_finish_time'], arguments['--area_code'], arguments['--authorization_header'])
