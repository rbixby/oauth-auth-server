from flask import (
    Flask,
    request,
)
# from flask_restful import Api
# from flask_talisman import Talisman
# from service.routes import add_resources
from service.routes import add_endpoints
from service.config import get_config

from . import logger

# import redis
import gzip


def create_app():
    # config = get_config()
    logger.info("Creating the app.")
    app = Flask(__name__)

    # Talisman(app, force_https=False)
    logger.info("Talisman is set up.")
    # api = Api(app, catch_all_404s=True)

    # app.config['redis'] = redis.StrictRedis(
    #     decode_responses=True,
    #     host=config['REDIS_HOST'],
    #     port=config['REDIS_PORT'])

    # add_resources(api)
    # app.add_endpoints()
    add_endpoints(app)

    def should_compress(response):
        config = get_config()
        return not response.direct_passthrough and all([
            len(response.data) > config['COMPRESS_MIN_SIZE'],
            'gzip' in request.headers.get('Accept-Encoding', '').lower(),  # pragma: no mutate
            'Content-Encoding' not in response.headers,
        ])

    @app.after_request
    def compress_response(response):
        if should_compress(response):
            response.data = gzip.compress(response.data, compresslevel=6)  # pragma: no mutate
            response.headers['Content-Encoding'] = 'gzip'

        return response

    @app.after_request
    def write_server_header(response):
        response.headers['Server'] = 'Roger'
        return response

    @app.teardown_request
    def log_uncaught_exceptions(error):
        if error is not None:
            logger.exception('An uncaught exception has occurred.', exc_info=error)

    return app
