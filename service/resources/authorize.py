# import requests
import uuid
from flask import request, render_template, make_response
from flask_restful import Resource
from service import logger

CLIENTS = [{"client_id": "oauth-client-1",
            "client_secret": "oauth-client-secret-1",
            "redirect_uris": ["http://localhost:9000/callback"],
            "scope": "foo bar"}]

CODES = {}


class AuthorizationServer(Resource):
    def __init__(self):
        self.clients = CLIENTS

    def post(self):
        logger.info("Received a POST.")
        return render_template("error.html", error="Not the correct action.")

    def get(self):
        logger.info("Received a GET.")
        # headers = {'Contentf-Type': 'text/html'}
        resp = {}
        if request.args:
            resp["resquest.args"] = "True"

        resp["got"] = "here"

        return resp
        # return make_response(render_template("error.html", error="Got here!"), 200, headers)
        # for k, v in request.args:
        #     logger.info("Key: {}, Value: {}".format(k, v))

        # client = self.get_client(request.args["client_id"])
        # if not client:
        #     # Check for known client
        #     logger.error('Unknown client %s', request.args['client_id'])
        #     render_template("error.html", error="Unknown client.")
        # elif request.args["redirect_uri"] not in client:
        #     logger.error("Mismatched redirect URI, expected %s got %s", client["redirect_uris"], request.args["redirect_uri"])
        #     render_template("error.html", error="Invalid redirect URI.")
        # else:
        #     render_template("error.html", error="I got here.")
        # Check for the scopes
        # req_scope = None
        # client_scope = client["scope"].split(" ")
        # if request.args['scope']:
        #     req_scope = request.args['scope'].split(' ')

        # same = [item for item in req_scope if item in client_scope]
        # if len(same) == 0:
        #     # client asked for a scope it could not have
        #     params = {"error": "invalid_scope"}
        #     callback_url = request.args['redirect_uri']
        #     response = requests.get(callback_url, params=params)
        #     response.history

        # auth_code = self.generate_auth_code()
        # CODES[auth_code]

    def get_client(self, args):
        if "client_id" in args:
            client_id = args["client_id"]
            for client in self.clients:
                if client_id in client.values():
                    return client
                else:
                    return None
        else:
            return None

    def generate_auth_code(self):
        auth_array = str(uuid.uuid4()).split("-")
        return auth_array[0]
