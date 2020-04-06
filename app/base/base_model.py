# -*- coding: utf-8 -*-
from datetime import datetime
from uuid import uuid4

import sqlalchemy as db


def stringify_uuid4():
    return str(uuid4())


class ModelBaseMixin:
    id = db.Column(db.String, default=stringify_uuid4, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)

    @staticmethod
    def flat_value(value):
        if isinstance(value, datetime):
            return str(value)
        return value

    def to_json(self):
        return {
            c.name: self.flat_value(getattr(self, c.name)) for c in self.__table__.columns
        }

    def fill(self, data: dict):
        for col in data:
            if col in self.__table__.columns:
                setattr(self, col, data[col])
