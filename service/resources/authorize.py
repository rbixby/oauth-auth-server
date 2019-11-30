import uuid
from flask import request, render_template, make_response
from flask_restful import Resource
from service import logger

CLIENTS = [{"client_id": "oauth-client-1",
            "client_secret": "oauth-client-secret-1",
            "redirect_uris": ["http://localhost:9000/callback"],
            "scope": "foo bar"}]

CODES = {}
REQUESTS = {}


class AuthorizationServer(Resource):
    def __init__(self):
        self.clients = CLIENTS

    def post(self):
        logger.info("Received a POST.")
        return render_template("error.html", error="Not the correct action.")

    def get(self):
        logger.info("Received a GET.")
        headers = {'Content-Type': 'text/html'}
        resp = {}
        if not request.args:
            resp["error"] = "Missing request parameters."
            return resp

        client = self.get_client(request.args)
        redirect_uri = self.get_redirect_uri(request.args, client)
        if not client:
            # Check for known client
            logger.error('Unknown client %s', request.args['client_id'])
            resp["error"] = "Unknown client."
            return resp
        elif not redirect_uri:
            logger.error("Mismatched redirect URI, expected %s got %s", client["redirect_uris"], request.args["redirect_uri"])
            resp["error"] = "Invalid redirect URI."
            return resp
        else:
            # Check for the scopes
            req_scope = None
            client_scope = client["scope"].split(" ")
            if request.args['scope']:
                req_scope = request.args['scope'].split(' ')

            same = [item for item in req_scope if item in client_scope]
            if len(same) == 0:
                # client asked for a scope it could not have
                resp["error"] = "invalid_scope"
                return resp

            reqid = self.generate_auth_code()
            REQUESTS[reqid] = request.path

            return make_response(render_template("authorize.html", reqid=reqid, scope=req_scope, client=client), 200, headers)
        # auth_code = self.generate_auth_code()
        # CODES[auth_code]

    def get_client(self, args):
        '''
        Gets and validates the client_id
        '''
        logger.info(type(args))
        logger.info("The request.args {}".format(args))
        if "client_id" in args:
            client_id = args["client_id"]
            for client in self.clients:
                if client_id in client.values():
                    return client
                else:
                    return None
        else:
            return None

    def get_redirect_uri(self, args, client):
        '''
        Gets and validates the redirect uri.
        '''
        if "redirect_uri" in args:
            redirect_uri = args["redirect_uri"]
            if redirect_uri in client["redirect_uris"]:
                return redirect_uri
            else:
                return None
        else:
            return None

    def generate_auth_code(self):
        auth_array = str(uuid.uuid4()).split("-")
        return auth_array[0]
