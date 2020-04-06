# -*- coding: utf-8 -*-
from sanic import Sanic, request
from sanic_openapi import swagger_blueprint

from . import helloworld, auth


def create_app(config_object) -> Sanic:
    app = Sanic(log_config=config_object.LOG_SETTINGS)
    app.config.from_object(config_object)
    register_routes(app)
    add_openapi(app)
    setup_app(app)

    return app


def register_routes(app):
    register_v1_routes(app)


def register_v1_routes(app):
    base_v1_url = '/api/1'

    helloworld.routes.setup_v1(base_v1_url, app)
    auth.routes.setup_v1(base_v1_url, app)


def add_openapi(app):
    if app.config.get('ENV') not in ['staging', 'prod']:
        app.blueprint(swagger_blueprint)


def setup_app(app):
    request.app = app
