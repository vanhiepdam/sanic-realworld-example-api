# -*- coding: utf-8 -*-
from sqlalchemy import event

from app.helpers import hash_string
from app.models import User


@event.listens_for(User, 'before_update')
@event.listens_for(User, 'before_insert')
def hash_password(mapper, connection, target):
    target.password = hash_string(target.password)

