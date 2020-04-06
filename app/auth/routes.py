# -*- coding: utf-8 -*-
from sanic_openapi import doc

from app.auth.views import AuthViewMixin, UserViewMixin
from app.base.base_view import ViewBaseMixin
from app.helpers import get_token_from_request
from app.middlewares import to_json_response, prevent_xss, add_cors_header, validate_access_token, permissions
from app.permissions import IsUserAdmin
from swagger.docs_auth import LoginConsume, LoginProduce


def setup_v1(base_url, app):
    auth_url = base_url + '/auth'

    @app.route(base_url + '/login', methods=['POST'])
    @doc.consumes(LoginConsume, location='body', required=True)
    @doc.produces(LoginProduce)
    @prevent_xss
    @add_cors_header(app)
    @to_json_response
    async def auth(request):
        data = request.json

        return AuthViewMixin.authenticate_user(data), 200

    @app.route(auth_url + '/renew_token', methods=['PUT'])
    @prevent_xss
    @add_cors_header(app)
    @to_json_response
    @validate_access_token
    async def renew_token(request):
        access_token = get_token_from_request(request)
        refresh_token = request.json.get('refresh_token')

        return AuthViewMixin.renew_token(access_token, refresh_token), 200

    @app.route(base_url + '/register', methods=['POST'])
    @add_cors_header(app)
    @to_json_response
    async def register(request):
        data = request.json
        user = AuthViewMixin.register_user(data)

        return user, 200

    @app.route(auth_url + '/users', methods=['GET'])
    @add_cors_header(app)
    @to_json_response
    async def list_users(request):
        limit = request.args.get('limit', ViewBaseMixin.LIMIT)
        offset = request.args.get('offset', ViewBaseMixin.OFFSET)

        users = UserViewMixin.list_users(criteria=None, limit=limit, offset=offset)

        return users, 200

    @app.route(auth_url + '/users/<user_id>', methods=['PATCH'])
    @add_cors_header(app)
    @to_json_response
    @validate_access_token
    async def update_user(request, user_id):
        data = request.json
        user = UserViewMixin.update(user_id, data)

        return user, 200

    @app.route(auth_url + '/users/<user_id>', methods=['GET'])
    @add_cors_header(app)
    @to_json_response
    @validate_access_token
    async def update_user(request, user_id):
        user = UserViewMixin.get_user(user_id)

        return user, 200

    @app.route(auth_url + '/users/<user_id>', methods=['DELETE'])
    @add_cors_header(app)
    @to_json_response
    @validate_access_token
    @permissions([IsUserAdmin])
    async def delete_user(request, user_id):
        response = UserViewMixin.delete_user(user_id)

        return response, 200
