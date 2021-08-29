"""
    define the api routes for your classes
"""

from flask import Blueprint
from flask_restful import Api

from .account import Account
from .session import Session
from .hello import HelloWorld, EchoWorld, ProtectedWorld
from .gamestate import GameState,GameStateReset, GameStateUpdate
from .teamsdata import TeamData,TeamsData

# endpoint routing errors, not the same as application level errors handled by the ResponseJson class
errors = {
    "Unauthorized": {
        "error": "Unauthorized Access",
        "status": 401
        },
    "NotFound": {
        "error": "Endpoint Not Found",
        "status": 404
        },
    "MethodNotAllowed": {
        "error": "Method Not Allowed",
        "status": 405
        }
}

demo_blueprint = Blueprint("demo_api", __name__)
demo_api = Api(demo_blueprint, errors=errors)

demo_api.add_resource(HelloWorld,"/hello")
demo_api.add_resource(ProtectedWorld,"/protectedhello")
demo_api.add_resource(Account,"/account")
demo_api.add_resource(Session,"/session")

demo_api.add_resource(GameState,"/gamestate/<gameid>")
demo_api.add_resource(GameStateUpdate,"/gamestate")
demo_api.add_resource(GameStateReset,"/gamestate/reset")
demo_api.add_resource(TeamsData,"/teams")
demo_api.add_resource(TeamData,"/teams/<gameid>")

