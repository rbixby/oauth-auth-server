from urllib import parse
from flask import request, redirect, render_template, make_response
from service.helpers.auth_helper import get_client_from_query, generate_auth_code, REQUESTS, CODES
from service import logger


def approve():
    logger.info("==> approve()")
    headers = {'Content-Type': 'text/html'}
    params = {}

    if not request.form:
        logger.error("Missing post parameters. Bad request.")
        return make_response(render_template('error.html', error='Missing post form parameters. Bad request.'), 400, headers)
        # return "Bad Request", 400
    else:
        query = REQUESTS.pop(request.form['reqid'], None)
        query = query.decode('UTF-8')
        print("The query: ", query)
        if not query:
            logger.error("Did not get a query string.")
            return make_response(render_template('error.html', error='Bad Request'), 400, headers)
        else:
            params = parse.parse_qs(query)
            print(params)
        if request.form["approve"]:
            logger.debug("Approving a token request.")
            if params["response_type"][0] == 'code':
                code = generate_auth_code()
                # Not sure whwer the user comes from.
                # user = request.form['user']

                scope = params['scope'][0]
                req_scope = scope.split(' ')

                client = get_client_from_query(params)
                print(client)
                client_scope = client['scope']

                same = [item for item in req_scope if item in client_scope]
                if len(same) == 0:
                    # Client asked for a scope it could not have.
                    return make_response(render_template('error.html', error='Invalid Scope'), 400, headers)

                # Save for later. A dictionary of stuff
                CODES[code] = {'authorizationRequest': query, 'scope': scope}

                # Build the redirect url
                redirect_uri = params['redirect_uri'][0]
                if redirect_uri not in client['redirect_uris']:
                    return make_response(render_template('error.html', error='Invalid redirect URI.'), 400, headers)

                state = params['state'][0]
                payload = {'code': code, 'state': state}

                the_location = ''.join((redirect_uri, '?', parse.urlencode(payload)))
                print(the_location)
                return redirect(the_location, code=302)

    return "Got here", 200
