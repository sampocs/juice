from flask import render_template, redirect, url_for
from flask.templating import render_template_string
from app import app
from .request_wrapper import http
from api import schemas as api_models

JUICE_API_ENDPOINT = 'http://api:8000'

def render_helper(page_name: str, **kwargs):
    current_week = 12
    template = f'{page_name}.html'
    past_weeks = range(1, current_week)
    upcoming_weeks = range(current_week, 17)
    return render_template(
        template, 
        tab=page_name, 
        past_weeks=past_weeks, 
        upcoming_weeks=upcoming_weeks,
        **kwargs)

@app.route('/')
def home():
    return redirect(url_for('season'))

@app.route('/season')
def season():
    try:
        response = http.get(f'{JUICE_API_ENDPOINT}/teams')
        teams = [api_models.Team(**t) for t in response.json() if t["active"]]
        teams = sorted(teams, key=lambda t: t.city)
        return render_helper('season', teams=teams)

    except Exception as e:
        print(str(e))
        return render_helper('error', message='Whoops! It appears the API is down.')

@app.route('/past/week=<week>')
def past(week):
    return render_helper('past')

@app.route('/upcoming/week=<week>')
def upcoming(week):
    return render_helper('upcoming')