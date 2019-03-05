from service.flask import create_app
from service import logger

application = create_app()

logger.debug("Application initialized.")
