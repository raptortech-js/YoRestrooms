from yotaxi import app
from flask import request, render_template
from API_KEY import api_token
import requests

YO_API = "https://api.justyo.co/yo/"


def send_yo(username, link):
    """Yo a username"""
    requests.post(
        YO_API,
        data={'api_token': api_token, 'username': username, 'link': link})


@app.route('/')
def main():
    """Index Controller"""
    return 'OK'
    #return render_template('index.html')


#@app.errorhandler(404)
def handle_error(e):
    return render_template('404.html')


@app.route('/noresult')
def noresult():
    return render_template('noresult.html')


@app.route('/yo')
def yo():
    """Handle callback request"""
    username = request.args.get('username')
    location = request.args.get('location')
    if location is None:
        send_yo(username, 'http://yo-restrooms.herokuapp.com/noresult')     
    else:
        splitted = location.split(';')
        latitude = splitted[0]
        longitude = splitted[1]
        link = ("http://www.refugerestrooms.org/restrooms?utf8=%E2%9C%93"
                "&search=Current+Location&lat={0}&long={1}").format(latitude, longitude)
        send_yo(username, link)
    return 'OK'
