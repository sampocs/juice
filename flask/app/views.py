from app import app
import os

@app.route('/')
def index():
    return '<h1>Juice</h1>'