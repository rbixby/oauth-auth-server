from urllib import parse
from flask import request, render_template, make_response
from service.helpers.auth_helper import generate_auth_code, REQUESTS, CODES
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

                # Save for later. A dictionary of stuff
                CODES[code] = {}

    return "Got here", 200
