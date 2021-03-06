from flask import request
import requests
import json
from flask_restful import Resource
from ..core.utils.responsejson import ResponseJson, MessageResponseJson
from ..extensions.decorators import require_password
from ..extensions.requestparser import RequestParser 


class TeamsData(Resource):
    def __init__(self):
        self.data_url_placeholder = "https://iplgame-dc13.restdb.io/rest/%s"
        self.headers = {
    'content-type': "application/json",
    'x-apikey': "bbb981b9fc2757c4de907a15523f7b47d1b9d",
    'cache-control': "no-cache"
    }
    
    def get(self):
        
        team_response = requests.request("GET", self.data_url_placeholder%("teamdata"), headers=self.headers)

        return team_response.json()


class TeamData(Resource):
    def __init__(self):
        self.data_url_placeholder = "https://iplgame-dc13.restdb.io/rest/%s"
        self.headers = {
    'content-type': "application/json",
    'x-apikey': "bbb981b9fc2757c4de907a15523f7b47d1b9d",
    'cache-control': "no-cache"
    }
    
    def get(self, gameid):

        gamestate_query_template = '{"gameid":"%s"}'
        teams_response = requests.request("GET", self.data_url_placeholder%("teamdata"), headers=self.headers, data=gamestate_query_template%(gameid))

        for team in teams_response.json():
            if team['gameid']==gameid:
                return team

        return {}