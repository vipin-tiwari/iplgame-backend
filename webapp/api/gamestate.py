from flask import request
import requests
import json
from flask_restful import Resource
from ..core.utils.responsejson import ResponseJson, MessageResponseJson
from ..extensions.decorators import require_password
from ..extensions.requestparser import RequestParser 


class GameState(Resource):
    def __init__(self):
        self.data_url_placeholder = "https://iplgame-dc13.restdb.io/rest/%s"
        self.headers = {
    'content-type': "application/json",
    'x-apikey': "bbb981b9fc2757c4de907a15523f7b47d1b9d",
    'cache-control': "no-cache"
    }
    
    def get(self):
        gamestate_response = requests.request("GET", self.data_url_placeholder%("gamestate"), headers=self.headers)

        team_response = requests.request("GET", self.data_url_placeholder%("teamdata"), headers=self.headers)

        response = gamestate_response.json()
        response[0]['teams'] = team_response.json()
        return response

    def post(self):
        parser = RequestParser()
        parser.add_argument("bidvalue", type=int, required=True, location="form")
        parser.add_argument("bidwinningteam", type=str, required=True, location="form")
        parser.add_argument("playerId", type=int, required=True, location="form")
        parser.add_argument("role", type=str, required=True, choices=("bowler", "batsmen", "allrounder", "wicketkeeper"), location="form")
        args = parser.parse_args()
        print(args)

        #Add Player to Team

        # Remove Player frmo unsold Item
        gamestate_response = requests.request("GET", self.data_url_placeholder%("gamestate"), headers=self.headers)
        current_gamestate = gamestate_response.json()[0]
        print(current_gamestate)
        print(current_gamestate['_id'])
        obj_id = current_gamestate['_id']

        team_query_template = '{"name":"%s"}'
        response = requests.request("GET", self.data_url_placeholder%("teamdata"), headers=self.headers, data=team_query_template%(args.bidwinningteam))
        teams_data = response.json()

        teams_response = None
        for item in teams_data:
            if item['name']==args.bidwinningteam:
                teams_response = item
                break


        print("Winning Team ===>")
        print(teams_response)
        teams_response['players'].append(args.playerId)
        teams_response['balanceAmount']=teams_response['balanceAmount']-args.bidvalue
        team_id=teams_response['_id']

        if args.role == 'bowler':
            current_gamestate['unsoldPlayers']['bowler'] = [i for i in current_gamestate['unsoldPlayers']['bowler'] if not (i['id'] == args.playerId)] 
            current_gamestate['counts']['bowlerSold'] = current_gamestate['counts']['bowlerSold'] +1

            teams_response['counts']['bowler'] = teams_response['counts']['bowler']+1

        elif args.role == 'batsmen':
            current_gamestate['unsoldPlayers']['batsmen'] = [i for i in current_gamestate['unsoldPlayers']['batsmen'] if not (i['id'] == args.playerId)] 
            current_gamestate['counts']['batsmenSold'] = current_gamestate['counts']['batsmenSold'] +1


            teams_response['counts']['batsmen'] = teams_response['counts']['batsmen']+1

        elif args.role == 'allrounder':
            current_gamestate['unsoldPlayers']['allrounder'] = [i for i in current_gamestate['unsoldPlayers']['allrounder'] if not (i['id'] == args.playerId)] 
            current_gamestate['counts']['allrounderSold'] = current_gamestate['counts']['allrounderSold'] +1

            teams_response['counts']['allrounder'] = teams_response['counts']['allrounder']+1

        elif args.role == "wicketkeeper":
            current_gamestate['unsoldPlayers']['wicketkeeper'] = [i for i in current_gamestate['unsoldPlayers']['wicketkeeper'] if not (i['id'] == args.playerId)] 
            current_gamestate['counts']['wicketkeeperSold'] = current_gamestate['counts']['wicketkeeperSold'] +1

            teams_response['counts']['wicketkeeper'] = teams_response['counts']['wicketkeeper']+1

        #Update the Team data
        teamurl = "https://iplgame-dc13.restdb.io/rest/teamdata/"+str(team_id)
        response = requests.request("PUT", teamurl, data=json.dumps(teams_response), headers=self.headers)

        print(teams_response)
        print("Update team status")
        print(response.json())

        # Update Gamestate
        gameurl = "https://iplgame-dc13.restdb.io/rest/gamestate/"+str(obj_id)
        response = requests.request("PUT", gameurl, data=json.dumps(current_gamestate), headers=self.headers)

        print("Update GameState ")
        print(response.json())

        return response.json()




class GameStateReset(Resource):
    def __init__(self):
        self.data_url_placeholder = "https://iplgame-dc13.restdb.io/rest/%s"
        self.headers = {
    'content-type': "application/json",
    'x-apikey': "bbb981b9fc2757c4de907a15523f7b47d1b9d",
    'cache-control': "no-cache"
    }

    def _create_gamestate_from_basedata(self,basedata):
        gamestate={}
        batsmen=[]
        bowler=[]
        allrounder=[]
        wicketkeeper=[]

        for item in basedata:
            if item['role'] == 'Bowler': 
                bowler.append(item)
            elif item['role'] == 'Batsman': 
                batsmen.append(item)
            elif item['role'] == 'Allrounder':
                allrounder.append(item)
            elif item['role'] == 'W. Keeper':
                wicketkeeper.append(item)

        gamestate['batsmen']=batsmen
        gamestate['bowler']=bowler
        gamestate['allrounder']=allrounder
        gamestate['wicketkeeper']=wicketkeeper

        return gamestate



    def get(self):
        r = ResponseJson({"message": "hello, world"})
        

        #Fetch BaseDate
        response = requests.request("GET", self.data_url_placeholder%("basedata"), headers=self.headers)
        basedata = response.json()

        basedata_gamestate = self._create_gamestate_from_basedata(basedata)
        #Fetch ObjectId of Gamestate Data
        response = requests.request("GET", self.data_url_placeholder%("gamestate"), headers=self.headers)
        current_gamestate = response.json()
        print(current_gamestate)
        print(current_gamestate[0]['_id'])
        obj_id = current_gamestate[0]['_id']

        gamestate_payload = {}
        gamestate_payload['roundNo'] = 0
        gamestate_payload['counts'] = {}
        gamestate_payload['counts']['total'] = len(basedata)
        gamestate_payload['counts']['batsmenSold'] = 0
        gamestate_payload['counts']['bowlerSold'] = 0
        gamestate_payload['counts']['allrounderSold'] = 0
        gamestate_payload['counts']['wicketkeeperSold'] = 0
        gamestate_payload['counts']['wicketkeeperTotal'] = len(basedata_gamestate['wicketkeeper'])
        gamestate_payload['counts']['allrounderTotal'] = len(basedata_gamestate['allrounder'])
        gamestate_payload['counts']['bowlerTotal'] = len(basedata_gamestate['bowler'])
        gamestate_payload['counts']['batsmenTotal'] = len(basedata_gamestate['batsmen'])
        gamestate_payload['teams'] = []
        gamestate_payload['unsoldPlayers'] = {}
        gamestate_payload['unsoldPlayers']['batsmen'] = basedata_gamestate['batsmen']
        gamestate_payload['unsoldPlayers']['bowler'] = basedata_gamestate['bowler']
        gamestate_payload['unsoldPlayers']['allrounder'] = basedata_gamestate['allrounder']
        gamestate_payload['unsoldPlayers']['wicketkeeper'] = basedata_gamestate['wicketkeeper']
        



        #Set the states
        payload = json.dumps(gamestate_payload)
        response = requests.request("PUT", str(self.data_url_placeholder%("gamestate"))+"/"+str(obj_id), data=payload, headers=self.headers)

        return response.json()



        #reset the gamestate 
