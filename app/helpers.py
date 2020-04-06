# -*- coding: utf-8 -*-
import bcrypt
from sanic import request as sanic_request

from app.config import DevConfig, StagingConfig, ProdConfig, LocalConfig
from app.exceptions import InvalidRequestParameter


def get_config_object(env):
    if env == 'dev':
        return DevConfig()
    elif env == 'staging':
        return StagingConfig()
    elif env == 'prod':
        return ProdConfig()
    else:
        return LocalConfig()


def hash_string(string: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(string.encode(), salt).decode()


def check_hash_string(string: str, hashed: str) -> bool:
    return bcrypt.checkpw(string.encode(), hashed.encode())


def get_token_from_request(request):
    token = request.headers.get('authorization')

    if token.startswith('Bearer '):
        return token.replace('Bearer ', '')

    raise InvalidRequestParameter('Token')


def get_app_config(config):
    return getattr(sanic_request, 'app').config[config]
