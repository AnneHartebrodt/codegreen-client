"""Usage: sleep_until.py -s <hours> -m <minutes> -p <percent_renewable> -f <hard_finish_time> -c <area_code> -a <authorization_header> 

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
from carbonaware.utils import sleep_until



if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1')
    print(arguments)
    print('Using carbonaware')
    d = "2023-06-07 18:00"
    date_format = "%Y-%m-%d %H:%M"
    finish_time = datetime.strptime( d,date_format)


    sleep_until(arguments['--hours'], arguments['--minutes'], arguments['--percent_renewable'], finish_time, arguments['--area_code'], arguments['--authorization_header'])
