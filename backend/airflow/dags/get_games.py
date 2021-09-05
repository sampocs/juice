import pandas as pd
from datetime import datetime

def get_team_id_mapping():
    teams = pd.read_sql('airflow/data/teams.csv')
    teams = teams[teams.active][['team_id', 'city', 'mascot']]
    teams_mapping = {
        f'{city} {mascot}': team_id for (_, (team_id, city, mascot)) in teams.iterrows()
    }
    return teams_mapping

