# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
from datetime import datetime, timezone

import jwt

from app.base.base_service import ServiceBaseMixin
from app.database import session_connect
from app.exceptions import UnauthenticatedException, InvalidRequestParameter
from app.helpers import hash_string, check_hash_string, get_app_config
from app.models.auth import User


class AuthenticationServiceMixin(ServiceBaseMixin):
    model = User
    token_exp_duration = 60 * 60

    @staticmethod
    def validate_token(access_token):
        payload = jwt.decode(
            jwt=access_token,
            key=get_app_config('APP_PUBLIC_KEY'),
            algorithm='RS256'
        )

        return payload

    @classmethod
    def generate_tokens(cls, user_data: dict):
        access_token = cls.generate_access_token(user_data)

        return {
            'access_token': access_token,
            'refresh_token': cls.generate_refresh_token(access_token)
        }

    @classmethod
    def generate_access_token(cls, user_data: dict):
        payload = {
            'user_id': user_data.get('id') or user_data.get('user_id'),
            'exp': int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()) + cls.token_exp_duration
        }
        # jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))
        access_token = jwt.encode(payload, key=get_app_config('APP_PRIVATE_KEY'), algorithm='RS256')

        return access_token

    @staticmethod
    def generate_refresh_token(access_token):
        if isinstance(access_token, str):
            access_token = access_token.encode('utf-8')
        digest = hmac.new(
            key=get_app_config('APP_PRIVATE_KEY').encode('utf-8'),
            msg=access_token,
            digestmod=hashlib.sha256
        ).digest()

        return base64.b64encode(
            digest,
            altchars="AA".encode("utf-8")
        ).decode()

    @classmethod
    def renew_token(cls, access_token, refresh_token):
        if cls.generate_refresh_token(access_token) == refresh_token:
            return cls.generate_tokens(user_data=cls.validate_token(access_token))

        raise InvalidRequestParameter('refresh_token')


class UserServiceMixin(ServiceBaseMixin):
    model = User

    @classmethod
    def validate_user_credentials(cls, username: str, password: str):
        with session_connect() as session:
            user = session.query(cls.model).filter(cls.model.username == username).first()

        if user and cls.check_password(password, user.password):
            return user.to_json()

        raise UnauthenticatedException

    @classmethod
    def set_password(cls, password: str):
        return hash_string(password)

    @classmethod
    def check_password(cls, raw: str, hashed: str):
        return check_hash_string(raw, hashed)
