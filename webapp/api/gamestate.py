from flask import request
import requests
import json
import uuid
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

    def _find_game_details(self, gameid):
        games_details = requests.request("GET", "https://iplgame-dc13.restdb.io/rest/gamestate", headers=self.headers )
        

        for game_info in games_details.json():
            print(game_info.keys())
            if game_info['gameid']==gameid:
                return game_info

        return []

    def _find_team_details(self, gameid):
        teams_details = requests.request("GET", "https://iplgame-dc13.restdb.io/rest/teamdata", headers=self.headers )
        
        for team_info in teams_details.json():
            if team_info['gameid']==gameid:
                return team_info['teams']

        return []
    
    def get(self, gameid):
        
        
        current_gamestate = self._find_game_details(gameid)

        current_gamestate['teams'] = self._find_team_details(gameid)
        return current_gamestate

class GameStateUpdate(Resource):
    def __init__(self):
        self.data_url_placeholder = "https://iplgame-dc13.restdb.io/rest/%s"
        self.headers = {
    'content-type': "application/json",
    'x-apikey': "bbb981b9fc2757c4de907a15523f7b47d1b9d",
    'cache-control': "no-cache"
    }

    def _find_player_info(self, playerId):
        
        players = requests.request("GET", "https://iplgame-dc13.restdb.io/rest/basedata", headers=self.headers )
        
        for player in players.json():
            if player['Id']==playerId:
                return player

        return {}

    def _find_team_details(self, gameid):
        teams_details = requests.request("GET", "https://iplgame-dc13.restdb.io/rest/teamdata", headers=self.headers )
        
        for team_info in teams_details.json():
            if team_info['gameid']==gameid:
                return team_info

        return []

    def _find_gamestate_details(self, gameid):
        gamestate_details = requests.request("GET", "https://iplgame-dc13.restdb.io/rest/gamestate", headers=self.headers )
        
        for gamestate_info in gamestate_details.json():
            if gamestate_info['gameid']==gameid:
                return gamestate_info

        return {}

    def post(self):
        parser = RequestParser()
        parser.add_argument("gameid", type=str, required=True, location="json")
        parser.add_argument("bidvalue", type=int, required=True, location="json")
        parser.add_argument("bidwinningteam", type=str, required=True, location="json")
        parser.add_argument("playerId", type=int, required=True, location="json")
        parser.add_argument("role", type=str, required=True, choices=("bowler", "batsmen", "allrounder", "wicketkeeper"), location="json")
        args = parser.parse_args()
        print("printing args")
        print(args)

        
        current_gamestate = self._find_gamestate_details(args.gameid)
        obj_id = current_gamestate['_id']

        teams_data = self._find_team_details(args.gameid)

        print("============")

        print(teams_data)

        print("============")
        print(len(teams_data['teams']))
        team_obj_id = teams_data['_id']

        winning_team_details = None
        
        for item in teams_data['teams']:
            if item['name']==args.bidwinningteam:
                winning_team_details = item
                break

        teams_data['teams'].remove(winning_team_details)

        print("Winning Team ===>")
        
        bid_player_detail = self._find_player_info(args.playerId)

        bid_player_detail.pop("_id")

        print(bid_player_detail)

        players = winning_team_details['players']
        players.append(bid_player_detail)

        print("======print(players)========")
        print(players)
        print("===================")
        
        winning_team_details['players'] = players

        winning_team_details['balanceAmount']=winning_team_details['balanceAmount']-args.bidvalue

        print(winning_team_details)

        if args.role == 'bowler':
            current_gamestate['unsoldPlayers']['bowler'] = [i for i in current_gamestate['unsoldPlayers']['bowler'] if not (i['Id'] == args.playerId)] 
            current_gamestate['counts']['bowlerSold'] = current_gamestate['counts']['bowlerSold'] +1
            winning_team_details['counts']['bowler'] = winning_team_details['counts']['bowler']+1

        elif args.role == 'batsmen':
            current_gamestate['unsoldPlayers']['batsmen'] = [i for i in current_gamestate['unsoldPlayers']['batsmen'] if not (i['Id'] == args.playerId)] 
            current_gamestate['counts']['batsmenSold'] = current_gamestate['counts']['batsmenSold'] +1


            winning_team_details['counts']['batsmen'] = winning_team_details['counts']['batsmen']+1

        elif args.role == 'allrounder':
            current_gamestate['unsoldPlayers']['allrounder'] = [i for i in current_gamestate['unsoldPlayers']['allrounder'] if not (i['Id'] == args.playerId)] 
            current_gamestate['counts']['allrounderSold'] = current_gamestate['counts']['allrounderSold'] +1

            winning_team_details['counts']['allrounder'] = winning_team_details['counts']['allrounder']+1

        elif args.role == "wicketkeeper":
            current_gamestate['unsoldPlayers']['wicketkeeper'] = [i for i in current_gamestate['unsoldPlayers']['wicketkeeper'] if not (i['Id'] == args.playerId)] 
            current_gamestate['counts']['wicketkeeperSold'] = current_gamestate['counts']['wicketkeeperSold'] +1

            winning_team_details['counts']['wicketkeeper'] = winning_team_details['counts']['wicketkeeper']+1

        teams_data['teams'].append(winning_team_details)

        print("team_obj_id: "+str(team_obj_id))
        #Update the Team data
        teamurl = "https://iplgame-dc13.restdb.io/rest/teamdata/"+str(team_obj_id)
        response = requests.request("PUT", teamurl, data=json.dumps(teams_data), headers=self.headers)

        print("Update team status")
        
        # Update Gamestate
        gameurl = "https://iplgame-dc13.restdb.io/rest/gamestate/"+str(obj_id)
        response = requests.request("PUT", gameurl, data=json.dumps(current_gamestate), headers=self.headers)

        print("Update GameState ")
        
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
            print(item)
            if item['Role'] == 'Bowler': 
                bowler.append(item)
            elif item['Role'] == 'Batsman': 
                batsmen.append(item)
            elif item['Role'] == 'All-rounder':
                allrounder.append(item)
            elif item['Role'] == 'Wicketkeeper-batsman':
                wicketkeeper.append(item)

        gamestate['batsmen']=batsmen
        gamestate['bowler']=bowler
        gamestate['allrounder']=allrounder
        gamestate['wicketkeeper']=wicketkeeper

        return gamestate



    def get(self):
        
        #Fetch BaseDate
        response = requests.request("GET", self.data_url_placeholder%("basedata"), headers=self.headers)
        basedata = response.json()

        new_game_id = str(uuid.uuid4())

        basedata_gamestate = self._create_gamestate_from_basedata(basedata)
        
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

        gamestate_payload['gameid'] = new_game_id

        



        #Set the states
        payload = json.dumps(gamestate_payload)
        gamestate_response = requests.request("POST", str(self.data_url_placeholder%("gamestate")), data=payload, headers=self.headers)


        base_teams_response = requests.request("GET", self.data_url_placeholder%("baseteam"), headers=self.headers)
        
        teams_response_new = {}
        teams_response_new['gameid']=new_game_id
        teams_response_new['teams']=base_teams_response.json()


        #Set the teams
        payload = json.dumps(teams_response_new)
        teams_response = requests.request("POST", str(self.data_url_placeholder%("teamdata")), data=payload, headers=self.headers)
        print(teams_response.json())
        

        return gamestate_response.json()



        #reset the gamestate 
