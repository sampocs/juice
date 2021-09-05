from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
import pandas as pd
import requests
import os

default_args = {
    'owner': 'sampocs'
}

API_ENDPOINT = os.environ['JUICE_API_ENDPOINT']

@dag(default_args=default_args, schedule_interval=None, start_date=days_ago(1))
def upload_teams():

    @task()
    def upload():
        print('Reading data into pandas...')
        df = pd.read_csv('/opt/airflow/data/teams.csv')
        rows = df.to_dict('records')

        print('Writing to database...')
        res = requests.post(f'{API_ENDPOINT}/teams', json=rows)

        assert res.status_code == 200, f'API Error {res.status_code}'
 
        print('Response:')
        print(res.json())

        print('Done.')

        return 

    upload()

upload_teams = upload_teams()