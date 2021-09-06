from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import os
from typing import Dict


default_args = {
    'owner': 'sampocs'
}

API_ENDPOINT = os.environ['JUICE_API_ENDPOINT']
YEAR = 2021

def scrape_regular_season_games(year: int) -> pd.DataFrame:
    """
    Scrapes the regular season games from Pro Football Reference 
    """
    df = pd.read_html(f"https://www.pro-football-reference.com/years/{year}/games.htm")[0]    

    # Remove header rows between weeks
    df = df[df.Week != 'Week']

    # Remove preseason games
    df = df[df['Week'].str.startswith('Pre') == False]

    # Fix columns
    df = df.drop(columns='Unnamed: 5')
    df.columns = ['week', 'dow', 'date', 'away_team', 'away_score', 'home_team', 'home_score', 'time']

    # Add season (year) and week columns
    df['season'] = year
    df['week'] = df['week'].astype('int')

    return df


def get_team_name_mapping() -> Dict:
    """
    Reads the CSV file that contains each team and returns a dictionary that maps each 
    team's full name to it's team_id
    """
    teams = pd.read_csv('/opt/airflow/data/teams.csv')
    teams = teams[teams.active][['team_id', 'city', 'mascot']]

    teams_mapping = {
        f'{city} {mascot}': team_id for (_, (team_id, city, mascot)) in teams.iterrows()
    }

    return teams_mapping


def format_for_db(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """
    Formats the dataframe with the columns needed in the database
    """
    def _to_datetime(row: pd.Series) -> datetime:
        """
        Converts the date and time columns into a single datetime column
        """
        date_string = row['date']
        time_string = row['time']
        
        month = datetime.strptime(date_string, '%B %d').month
        if month < 3:
            date_string += f' {year + 1}'
        else:
            date_string += f' {year}'
            
        datetime_string = f'{date_string} {time_string}'
            
        dt = datetime.strptime(datetime_string, '%B %d %Y %H:%M %p')

        return dt
    
    
    def _add_game_id(row: pd.Series) -> str:
        """
        Adds the game id which is a concatenation of the date and home team ID
        """
        date = row['datetime'].strftime('%Y%m%d')
        home_team_id = row['home_team_id']

        return f'{date}_{home_team_id}'

    # Add the team IDs from full team name
    team_name_mapping = get_team_name_mapping()

    df['home_team_id'] = df['home_team'].apply(lambda team_name: team_name_mapping[team_name])
    df['away_team_id'] = df['away_team'].apply(lambda team_name: team_name_mapping[team_name])

    # Add a datetime and game_id column
    df['datetime'] = df.apply(_to_datetime, axis=1)
    df['game_id'] = df.apply(_add_game_id, axis=1)

    # Fill all NaN's with None for the API
    df = df.replace({np.nan:None})

    # Caat the datetime to a string
    df['datetime'] = df['datetime'].apply(lambda dt: datetime.strftime(dt, '%Y-%m-%d %H:%M:%S'))

    df = df[[
        'game_id', 'season', 'week', 'datetime', 'home_team_id', 'away_team_id', 'home_score', 'away_score'
    ]]

    return df

@dag(default_args=default_args, schedule_interval=None, start_date=days_ago(1))
def upload_games():

    @task()
    def upload():
        print('Scraping from PFR')
        df = scrape_regular_season_games(YEAR)
        df = format_for_db(df, YEAR)
        rows = df.to_dict('records')

        print('Writing to database...')
        res = requests.post(f'{API_ENDPOINT}/games', json=rows)

        assert res.status_code == 200, f'API Error {res.status_code}'
 
        print('Response:')
        print(res.json())

        print('Done.')

        return 

    upload()

upload_games = upload_games()