# -*- coding: utf-8 -*-
import logging
import traceback

from sanic import request as sanic_request
from sanic.response import json
from sqlalchemy.orm import Session

from app.exceptions import ExceptionBase, UnauthenticatedException, PermissionDeniedException
from app.helpers import get_token_from_request

logger = logging.getLogger(__name__)


def to_json_response(func):
    async def inner(*args, **kwargs):
        try:
            result, status_code = await func(*args, **kwargs)

            return json(result, status=status_code)
        except ExceptionBase as ex:
            data = ex.to_api_response()
            status_code = ex.code
            logger.error(traceback.format_exc())

            return json(data, status=status_code)
        except Exception as ex:
            logger.error(traceback.format_exc())

            return json({
                'detail': 'Internal server error: %s' % str(ex),
                'code': 500,
            }, 500)
        finally:
            if isinstance(hasattr(sanic_request, 'session'), Session):
                getattr(sanic_request, 'session').close()

    inner.__name__ = func.__name__

    return inner


def add_cors_header(app):
    def func(f):
        async def inner(*args, **kwargs):
            response = await f(*args, **kwargs)
            response.headers['Access-Control-Allow-Origin'] = app.config.get('ALLOWED_HOSTS', '*')
            response.headers['Access-Control-Allow-Credentials'] = True

            return response

        inner.__name__ = func.__name__
        return inner

    return func


def prevent_xss(func):
    async def inner(*args, **kwargs):
        response = await func(*args, **kwargs)
        response.headers["x-xss-protection"] = "1; mode=block"
        return response

    inner.__name__ = func.__name__

    return inner


def validate_access_token(func):
    async def inner(request, *args, **kwargs):
        from app.auth.services import AuthenticationServiceMixin
        from app.auth.services import UserServiceMixin

        access_token = get_token_from_request(request)

        payload = AuthenticationServiceMixin.validate_token(access_token)
        if access_token and payload:
            sanic_request.user = UserServiceMixin.get_by_id(payload['user_id'])
            return await func(request, *args, **kwargs)

        raise UnauthenticatedException

    inner.__name__ = func.__name__

    return inner


def permissions(permission_classes):
    def func(f):
        async def inner(*args, **kwargs):
            has_permission = all([cls.has_permission() for cls in permission_classes])

            if not has_permission:
                raise PermissionDeniedException

            return await f(*args, **kwargs)

        func.__name__ = f.__name__

        return inner
    return func
