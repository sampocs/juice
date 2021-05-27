from flask import render_template, redirect, url_for
from app import app

SEASONS = [2018, 2019]

def render_helper(page_name, **kwargs):
    current_season = 2019
    current_week = 12
    template = f'{page_name}.html'
    past_weeks = range(1, current_week)
    upcoming_weeks = range(current_week, 17)
    return render_template(
        template, 
        tab=page_name, 
        past_weeks=past_weeks, 
        upcoming_weeks=upcoming_weeks)


@app.route('/')
def home():
    return redirect(url_for(f'season'))

@app.route('/season')
def season():
    past_weeks = range(1, 9)
    upcoming_weeks = range(9, 17)
    return render_template('season.html', tab="season", past_weeks=past_weeks, upcoming_weeks=upcoming_weeks)

