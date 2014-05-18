#!/usr/bin/python

import requests
import json

url = 'http://127.0.0.1:8000'
username = 'raphael'
password = 'test'


def get_auth_token(url, username, password):
    auth_obj = json.dumps({'username': username, 'password': password})
    session = requests.Session()
    session.headers.update(
        {'Accept': 'application/json', 'Content-Type': 'application/json'})

    return session.post(url + '/api-token-auth/', auth_obj)

if __name__ == '__main__':
    response = get_auth_token(url, username, password)
    try:
        token = response.json()['token']
        print(token)
    except:
        print(response.json())
