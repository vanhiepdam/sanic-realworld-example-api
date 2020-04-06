# -*- coding: utf-8 -*-
from app.auth.services import UserServiceMixin, AuthenticationServiceMixin
from app.base.base_view import ViewBaseMixin


class UserViewMixin(ViewBaseMixin):
    @classmethod
    def list_users(cls, criteria, limit, offset):
        users = UserServiceMixin.list(criteria)
        count = users.count()
        paginated_users = UserServiceMixin.paginate_query(users, limit, offset)
        items = [user.to_json() for user in paginated_users]

        return cls.get_pagination_result(items, count, limit, offset)

    @classmethod
    def update(cls, user_id, data):
        user = UserServiceMixin.update_by_id(user_id, data)

        return user.to_json()

    @classmethod
    def get_user(cls, user_id):
        user = UserServiceMixin.get_by_id(user_id)

        return user.to_json()

    @classmethod
    def delete_user(cls, user_id):
        UserServiceMixin.delete(user_id)

        return cls.deleted_message(user_id)


class AuthViewMixin(ViewBaseMixin):
    @classmethod
    def register_user(cls, data):
        user = UserServiceMixin.create(data)

        return user.to_json()

    @classmethod
    def authenticate_user(cls, data):
        username = data.get('username', '')
        password = data.get('password', '')

        user = UserServiceMixin.validate_user_credentials(username, password)
        credentials = AuthenticationServiceMixin.generate_tokens(user)

        return credentials

    @classmethod
    def renew_token(cls, access_token, refresh_token):
        credentials = AuthenticationServiceMixin.renew_token(access_token, refresh_token)

        return credentials
