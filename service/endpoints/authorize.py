from flask import request, render_template, make_response
from service.helpers.auth_helper import get_client, get_redirect_uri, generate_auth_code
from service import logger

CLIENTS = [{"client_id": "oauth-client-1",
            "client_secret": "oauth-client-secret-1",
            "redirect_uris": ["http://localhost:9000/callback"],
            "scope": "foo bar"}]

CODES = {}
REQUESTS = {}


def authorize():
    logger.info("Inside authorize")
    headers = {'Content-Type': 'text/html'}
    resp = {}
    if not request.args:
        resp["error"] = "Missing request parameters."
        return resp

    client = get_client(request.args)
    redirect_uri = get_redirect_uri(request.args, client)
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

        reqid = generate_auth_code()
        REQUESTS[reqid] = request.path

        return make_response(render_template("authorize.html", reqid=reqid, scope=req_scope, client=client), 200, headers)

    # auth_code = self.generate_auth_code()
    # CODES[auth_code]
