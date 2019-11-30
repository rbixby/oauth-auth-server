from flask import request, render_template, make_response
from service.helpers.auth_helper import get_client, get_redirect_uri, generate_auth_code, REQUESTS
from service import logger

CLIENTS = [{"client_id": "oauth-client-1",
            "client_secret": "oauth-client-secret-1",
            "redirect_uris": ["http://localhost:9000/callback"],
            "scope": "foo bar"}]


def authorize():
    logger.info("Inside authorize")
    headers = {'Content-Type': 'text/html'}
    resp = {}
    if not request.args:
        resp["error"] = "Missing request parameters."
        return make_response(render_template("error.html", error='Missing request parameters.'), 200, headers)

    client = get_client(request.args)
    redirect_uri = get_redirect_uri(request.args, client)
    if not client:
        # Check for known client
        logger.error('Unknown client %s', request.args['client_id'])
        resp["error"] = "Unknown client."
        return make_response(render_template("error.html", error='Unknown client.'), 400, headers)
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
            return make_response(render_template("error.html", error='Invalid Scope'), 400, headers)

        reqid = generate_auth_code()
        REQUESTS[reqid] = request.query_string

        return make_response(render_template("authorize.html", reqid=reqid, scope=req_scope, client=client), 200, headers)

    # auth_code = self.generate_auth_code()
    # CODES[auth_code]
