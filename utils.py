import pendulum
import constants
from typing import Tuple
import os
import psycopg2 as psql


def connect_to_postgres():

    conn = psql.connect(
        dbname='juice',
        user='juice',
        password=os.environ['JUICE_PASSWORD'],
        host='0.0.0.0',
        port=5432)

    cur = conn.cursor()

    return conn, cur


def get_week_number_from_date(date: pendulum.date) -> Tuple[int, int]:
    """
    Returns the season year and week number given a date
    """
    # Calculate the week number by checking how many days since 
    #  the start of the season
    season_start = pendulum.parse(constants.SEASON_START_DATE).date()
    duration = (date - season_start).in_days()
    week = (duration // 7) + 1

    # If we're at the start of the year, then we need to subtract a year
    #  to get the season's year 
    year = (date.year - 1) if date.month < 6 else date.year 

    return (year, week)


def get_current_week_number() -> Tuple[int, int]:
    """
    Returns current season year and week number
    """
    curr_date = pendulum.today(tz=constants.TIME_ZONE).date()
    return get_week_number_from_date(curr_date)