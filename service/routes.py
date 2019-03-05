from service.resources.authorize import AuthorizationServer


RESOURCES = [
    ('/authorize', AuthorizationServer)
]


def add_resources(api):
    for route, resource in RESOURCES:
        api.add_resource(resource, route)
