# from service.resources.authorize import AuthorizationServer
from service.endpoints.authorize import authorize
from service.endpoints.approve import approve
from service.endpoints.token import token
from service import logger


ENDPOINTS = [
    ('/authorize', 'authorize', authorize),
    ('/token', 'token', token)
    # ('/approve', 'approve', approve)
]

# Commenting out the RESTful stuff for now,
# May need it later.
# RESOURCES = [
#     ('/authorize', AuthorizationServer)
# ]


# def add_resources(api):
#     for route, resource in RESOURCES:
#         api.add_resource(resource, route)


def add_endpoints(app):
    logger.debug("Adding endpoint routes.")
    app.add_url_rule('/', 'root', lambda: 'ok')
    app.add_url_rule('/approve', 'approve', approve, methods=['GET', 'POST'])
    app.add_url_rule('/token', 'token', token, methods=['GET', 'POST'])
    app.add_url_rule("/authorize", "authorize", authorize, methods=['GET', 'POST'])

    # for route, endpoint, handler in ENDPOINTS:
    #     app.add_url_rule(route, endpoint, handler, methods=['GET', 'POST'])
