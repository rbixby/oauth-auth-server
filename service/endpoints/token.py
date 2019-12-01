import base64
from flask import request, make_response, render_template
from service.helpers.auth_helper import get_client_from_id
from service import logger


def token():
    headers = {'Content-Type': 'text/html'}
    req_headers = request.headers
    auth = req_headers['authorization']
    client_id = None
    client_secret = None

    if (auth):
        auth_string = auth.split(' ')[1]
        creds = auth_string.split(":")
        client_id = base64.b64decode(creds[0]).decode('utf-8')
        client_secret = base64.b64decode(creds[1]).decode('utf-8')

    if request.form['client_id']:
        if client_id:
            return 'Invalid client id.', 401

        client_id = request.form['client_id']
        client_secret = request.form['client_secret']

    client = get_client_from_id(client_id)

    if client is None:
        logger.info(f'Unknown client id: {client_id}')
        return 'Unknown client.', 401

    if client_secret != client['client_secret']:
        logger.warn('Mismatched client secret.')
        return 'Invalid client', 401

    return make_response(render_template('error.html', error='Not Supported Yet.'), 503, headers)
