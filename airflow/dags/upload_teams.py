from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
import pandas as pd
import os

default_args = {
    'owner': 'sampocs'
}

@dag(default_args=default_args, schedule_interval=None, start_date=days_ago(1))
def upload_teams():

    @task()
    def upload():
        from common.database.main import engine

        print('Reading data into pandas...')
        df = pd.read_csv('/opt/airflow/data/teams.csv')

        print('Writing to postgres...')
        df.to_sql(name='teams', con=engine, if_exists='replace', index=False)

        print('Done.')

        return 

    upload()

upload_teams = upload_teams()
