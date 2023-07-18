#!/usr/bin/env python 

import click
import requests
import time
from datetime import timedelta, datetime, timezone
import functools
import pandas as pd
from codegreen.decorators import sleep_until

from codegreen.config import get_api_endpoint, get_api_key
from urllib.parse import urljoin

API_URL = get_api_endpoint()
API_KEY = get_api_key()
AUTHORIZATION_HEADER = {'Authorization': API_KEY}


@click.group()
def codegreen():
    pass




@codegreen.command(
    "timeshift", short_help="Time shift, by sleeping until ready"
)
@click.option("-a",
    "--authorization_header", default=None, help="header"
)
@click.option(
    "-s",
    "--hours",
    default=2,
    help="Estimated run time hours",
)
@click.option(
    "-m",
    "--minutes",
    default=20,
    help="Estimated run time in minutes",
)
@click.option(
    "-p",
    "--percent_renewable", default=30, help="Required percentage of renewables"
)
@click.option(
    "-f"
    "--hard_finish_time", default="currentyear:currentmonth:currentday 18:00", help="Deadline (default today 18:00)"
)
@click.option(
    "-c",
    "--area-code", default=None, help="Area of compute as CountryISOCode-PostalCode e.g. DEU-97107, or DEU-9"
)
@click.option(
    "--logging/--no-logging", default=True, help="Allow API to log request (remains private)"
)
def timeshift(authorization_header, hours, minutes, percent_renewable, hard_finish_time, area_code, logging):
    sleep_until(authorization_header,
                hours, 
                minutes, 
                percent_renewable, 
                hard_finish_time, 
                area_code, 
                logging)

@codegreen.command(
    "upload", short_help="Run an infinite loop to monitor this machine."
)
@click.option(
    "--authorization_header", default=None, help="header"
)
@click.option(
    "--workflow_tracefile", default=None, help="Tracefile"
)
@click.option(
    "--workflow_manager", default=None, help="header"
)


def upload():
    pass

