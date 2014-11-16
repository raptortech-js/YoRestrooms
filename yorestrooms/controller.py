from yorestrooms import app
from flask import request, url_for, render_template
import os
import requests

api_token = os.environ['HEROKU_KEY']

YO_API = "https://api.justyo.co/yo/"
_refuge_restrooms_production = "http://refugerestrooms.org"

if 'RR_SERVER' in os.environ:
    REFUGE_RESTROOMS_BASE = os.environ[RR_SERVER]
else:
    REFUGE_RESTROOMS_BASE = _refuge_restrooms_production


def send_yo(username, link):
    """Yo a username"""
    requests.post(
        YO_API,
        data={'api_token': api_token, 'username': username, 'link': link})


@app.context_processor
def inject_refuge_restrooms_base():
    return dict(rrbase=REFUGE_RESTROOMS_BASE)


@app.route('/')
def main():
    """Index Controller"""
    return render_template('index.html')


@app.errorhandler(404)
def handle_error(e):
    return render_template('404.html')


@app.route('/nolocation')
def noresult():
    return render_template('noresult.html')


@app.route('/yo')
def yo():
    """Handle callback request"""
    username = request.args.get('username')
    location = request.args.get('location')

    URL_BASE = request.url_root[:-1]  # trim trailing slash
    if location is None:
        link = URL_BASE + url_for('noresult')
    else:
        splitted = location.split(';')
        latitude = splitted[0]
        longitude = splitted[1]
        link = ("{0}/restrooms?utf8=%E2%9C%93&search=Current+Location&lat={1}"
                "&long={2}").format(REFUGE_RESTROOMS_BASE, latitude, longitude)
    
    send_yo(username, link)
    return 'OK; sent link {0} to user {1}'.format(link, username)
