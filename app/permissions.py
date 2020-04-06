# -*- coding: utf-8 -*-
from sanic import request


class PermissionBase:
    @classmethod
    def has_permission(cls):
        raise NotImplemented


class IsAuthenticated(PermissionBase):
    @classmethod
    def has_permission(cls):
        return request.user


class IsUserAdmin(PermissionBase):
    @classmethod
    def has_permission(cls):
        return request.user.is_staff
