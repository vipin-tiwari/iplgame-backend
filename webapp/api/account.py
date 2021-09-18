from flask import request
from flask_restful import Resource
from ..core.utils.responsejson import ErrorResponseJson, ExceptionResponseJson
from ..extensions.requestparser import RequestParser
from ..extensions.decorators import require_auth_header, validate_json
from ..managers.accountmanager import AccountManager


class Account(Resource):

    @require_auth_header
    def post(self):
        parser = RequestParser()
        parser.add_argument("username", type=str, required=True, location="json")
        parser.add_argument("password", type=str, required=True, location="json")
        parser.add_argument("role", type=str, required=True, location="json")
        args = parser.parse_args()

        """ create a new user account """
        try:
            email = request.authorization.username
            password = request.authorization.password
            #role = request.authorization.role
            role='ADMIN'
            role=args.role

            print("Fetching Input : "+email+" : "+password+" : "+role)

            acct_manager = AccountManager()
            result = acct_manager.create(email, password, role)
            return result.make_response()

        except KeyError as e:
            return ErrorResponseJson("missing required key: {}".format(str(e))).make_response()
        except Exception as e:
            return ExceptionResponseJson(str(e), e).make_response()

