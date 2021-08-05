from flask import request
import requests
import json
from flask_restful import Resource
from ..core.utils.responsejson import ResponseJson, MessageResponseJson
from ..extensions.decorators import require_password
from ..extensions.requestparser import RequestParser 
import uuid
from pysondb import db


class GameState(Resource):
    def __init__(self):
        self.data_url_placeholder = "https://iplgame-dc13.restdb.io/rest/%s"
        self.basedata=db.getDb('./data/basedata.json')
        self.team_response=db.getDb('./data/teamdata.json')
        self.gamestate=db.getDb('./data/gamestate.json')
    
    def get(self):
        gamestate_response = self.gamestate.getAll()

        return gamestate_response

    def post(self):
        parser = RequestParser()
        parser.add_argument("gameid", type=int, required=True, location="json")
        parser.add_argument("bidvalue", type=int, required=True, location="json")
        parser.add_argument("bidwinningteam", type=str, required=True, location="json")
        parser.add_argument("playerId", type=int, required=True, location="json")
        parser.add_argument("role", type=str, required=True, choices=("bowler", "batsmen", "allrounder", "wicketkeeper"), location="json")
        args = parser.parse_args()
        print(args)

        #Add Player to Team

        # Remove Player frmo unsold Item
        gamestate_response = self.gamestate.getBy({"id":args.gameid})

        print(gamestate_response[0].keys())

        current_gamestate = gamestate_response[0]['state']

        current_gamestate_teamdata = current_gamestate['teams']

        for item in current_gamestate_teamdata[:]:
            if item['name']==args.bidwinningteam:
                teams_response = item
                current_gamestate_teamdata.remove(item)
        


        print("Winning Team ===>")
        print(teams_response)
        teams_response['players'].append(args.playerId)
        teams_response['balanceAmount']=teams_response['balanceAmount']-args.bidvalue
        team_id=teams_response['_id']

        if args.role == 'bowler':
            current_gamestate['unsoldPlayers']['bowler'] = [i for i in current_gamestate['unsoldPlayers']['bowler'] if not (i['Id'] == args.playerId)] 
            current_gamestate['counts']['bowlerSold'] = current_gamestate['counts']['bowlerSold'] +1

            teams_response['counts']['bowler'] = teams_response['counts']['bowler']+1

        elif args.role == 'batsmen':
            current_gamestate['unsoldPlayers']['batsmen'] = [i for i in current_gamestate['unsoldPlayers']['batsmen'] if not (i['Id'] == args.playerId)] 
            current_gamestate['counts']['batsmenSold'] = current_gamestate['counts']['batsmenSold'] +1


            teams_response['counts']['batsmen'] = teams_response['counts']['batsmen']+1

        elif args.role == 'allrounder':
            current_gamestate['unsoldPlayers']['allrounder'] = [i for i in current_gamestate['unsoldPlayers']['allrounder'] if not (i['Id'] == args.playerId)] 
            current_gamestate['counts']['allrounderSold'] = current_gamestate['counts']['allrounderSold'] +1

            teams_response['counts']['allrounder'] = teams_response['counts']['allrounder']+1

        elif args.role == "wicketkeeper":
            current_gamestate['unsoldPlayers']['wicketkeeper'] = [i for i in current_gamestate['unsoldPlayers']['wicketkeeper'] if not (i['Id'] == args.playerId)] 
            current_gamestate['counts']['wicketkeeperSold'] = current_gamestate['counts']['wicketkeeperSold'] +1

            teams_response['counts']['wicketkeeper'] = teams_response['counts']['wicketkeeper']+1

        
        current_gamestate_teamdata.append(teams_response)
        current_gamestate['teams'] = current_gamestate_teamdata

        self.gamestate.updateById(args.gameid,{"state":current_gamestate})

        print("Update GameState ")

        return current_gamestate_teamdata




class GameStateReset(Resource):
    def __init__(self):
        self.team_response=db.getDb('./data/teamdata.json')
        self.gamestate=db.getDb('./data/gamestate.json')
        self.basedata=db.getDb('./data/basedata.json')

    def _create_gamestate_from_basedata(self,basedata):
        gamestate={}
        batsmen=[]
        bowler=[]
        allrounder=[]
        wicketkeeper=[]

        for item in basedata:
            if item['Role'] == 'Bowler': 
                bowler.append(item)
            elif item['Role'] == 'Batsman': 
                batsmen.append(item)
            elif item['Role'] == 'Allrounder':
                allrounder.append(item)
            elif item['Role'] == 'W. Keeper':
                wicketkeeper.append(item)

        gamestate['batsmen']=batsmen
        gamestate['bowler']=bowler
        gamestate['allrounder']=allrounder
        gamestate['wicketkeeper']=wicketkeeper

        return gamestate



    def get(self):
        r = ResponseJson({"message": "hello, world"})
        

        #Fetch BaseDate
        basedata = self.basedata.getAll()

        team_response = self.team_response.getAll()

        basedata_gamestate = self._create_gamestate_from_basedata(basedata)

        new_game_id = str(uuid.uuid4())


        
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
        gamestate_payload['teams'] = team_response
        gamestate_payload['unsoldPlayers'] = {}
        gamestate_payload['unsoldPlayers']['batsmen'] = basedata_gamestate['batsmen']
        gamestate_payload['unsoldPlayers']['bowler'] = basedata_gamestate['bowler']
        gamestate_payload['unsoldPlayers']['allrounder'] = basedata_gamestate['allrounder']
        gamestate_payload['unsoldPlayers']['wicketkeeper'] = basedata_gamestate['wicketkeeper']
        



        #Set the states
        payload = json.dumps(gamestate_payload)

        generated_game_id = self.gamestate.add({"state":gamestate_payload})

        
        return self.gamestate.getBy({"id":generated_game_id})



        #reset the gamestate 
