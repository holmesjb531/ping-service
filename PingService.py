import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPDigestAuth
from requests.auth import HTTPDigestAuth as HttpAuth
import requests
import datetime


app = Flask(__name__)
auth = HTTPDigestAuth()

# Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Secret key'

usernamePassword = {
    'vcu': 'rams'
}

url = 'https://pong-holmesjb-cmsc455.herokuapp.com/pong'
# local_url = 'http://127.0.0.1:3000/pong'

@auth.get_password
def get_password(username):
    if username in usernamePassword:
        return usernamePassword.get(username)
    return None

@app.route('/ping', methods=['GET'])
@auth.login_required
def ping_service():

    username = auth.username()
    password = auth.get_password_callback(username)

    startTime = datetime.datetime.now()




    authpong = HttpAuth('vcu', 'rams')
    requestpong = requests.get(url, auth=requests.auth.HTTPDigestAuth(username, password))

    endTime = datetime.datetime.now()
    time_passed = endTime - startTime
    time_passed = time_passed.microseconds / 1000

    return jsonify({'pingpong_t': time_passed}), 201


if __name__ == '__main__':
    app.run()
