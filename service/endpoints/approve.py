# from flask import request, render_template, make_response
from service import logger


def approve():
    logger.info("==> approve()")
    return "Got here", 200
