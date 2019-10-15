from flask import request
# , render_template, make_response
from service.helpers.auth_helper import REQUESTS, CODES
from service.helpers.auth_helper import generate_auth_code
from service import logger


def approve():
    logger.info("==> approve()")
    # headers = {'Content-Type': 'text/html'}

    if not request.form:
        logger.error("Missing post parameters. Bad request.")
        return "Bad Request", 400

    else:
        query = REQUESTS.pop('reqid', None)
        if not query:
            logger.error("Did not get a query string.")
            return "Bad Request", 400

        if request.form["approve"]:
            logger.debug("Approving a token request.")
            if query["response_type"] == 'code':
                code = generate_auth_code()

                # Save for later. A dictionary of stuff
                CODES[code] = {}

    return "Got here", 200
