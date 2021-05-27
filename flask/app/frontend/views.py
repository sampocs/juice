from flask import render_template, redirect, url_for
from flask.templating import render_template_string
from app import app


def render_helper(page_name):
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
    return redirect(url_for('season'))

@app.route('/season')
def season():
    return render_helper('season')

@app.route('/past/week=<week>')
def past(week):
    return render_helper('past')

@app.route('/upcoming/week=<week>')
def upcoming(week):
    return render_helper('upcoming')