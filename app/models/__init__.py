# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


from app.models.auth import User, UserGroup, UserPermission, Group, Permission, GroupPermission
from app.auth.events import hash_password
