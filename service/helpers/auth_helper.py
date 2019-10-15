import uuid
from service import logger

REQUESTS = {}
CODES = {}

CLIENTS = [{"client_id": "oauth-client-1",
            "client_secret": "oauth-client-secret-1",
            "redirect_uris": ["http://localhost:9000/callback"],
            "scope": "foo bar"}]


def get_client(args):
    '''
    Gets and validates the client_id
    '''
    logger.info(type(args))
    logger.info("The request.args {}".format(args))
    if "client_id" in args:
        client_id = args["client_id"]
        for client in CLIENTS:
            if client_id in client.values():
                return client
            else:
                return None
    else:
        return None


def get_redirect_uri(args, client):
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


def generate_auth_code():
    auth_array = str(uuid.uuid4()).split("-")
    return auth_array[0]
