# -*- coding: utf-8 -*-
import sqlalchemy as db

from app.base.base_model import ModelBaseMixin
from app.models import Base


class Group(Base, ModelBaseMixin):
    __tablename__ = 'groups'

    name = db.Column(db.String, unique=True)


class Permission(Base, ModelBaseMixin):
    __tablename__ = 'permissions'

    name = db.Column(db.String)
    action = db.Column(db.String, index=True)
    on_table = db.Column(db.String, index=True)


class GroupPermission(Base, ModelBaseMixin):
    __tablename__ = 'groups_permissions'

    group_id = db.Column(db.ForeignKey('groups.id'))
    permission_id = db.Column('permission_id', db.ForeignKey('permissions.id'))

    _gp_combine_unique = db.UniqueConstraint('group_id', 'permission_id')


class User(Base, ModelBaseMixin):
    __tablename__ = 'users'

    username = db.Column(db.String, index=True, unique=True)
    email = db.Column(db.String, index=True, unique=True)
    password = db.Column(db.String)
    is_staff = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return "<User: {name}>".format(name=self.username)

    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'is_active': self.is_active
        }


class UserGroup(Base, ModelBaseMixin):
    __tablename__ = 'users_groups'

    user_id = db.Column(db.ForeignKey('users.id'))
    group_id = db.Column(db.ForeignKey('groups.id'))

    _ug_combine_unique = db.UniqueConstraint('user_id', 'group_id')


class UserPermission(Base, ModelBaseMixin):
    __tablename__ = 'users_permissions'

    user_id = db.Column(db.ForeignKey('users.id'))
    permission_id = db.Column(db.ForeignKey('permissions.id'))

    _up_combine_unique = db.UniqueConstraint('user_id', 'permission_id')
