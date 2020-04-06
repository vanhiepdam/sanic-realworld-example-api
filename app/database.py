# -*- coding: utf-8 -*-

from contextlib import contextmanager

from sanic import request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import create_postgresql_connection_string

engine = create_engine(create_postgresql_connection_string())

Session = sessionmaker(bind=engine)


@contextmanager
def session_connect():
    session = Session()
    try:
        yield session
        if not hasattr(request, 'app') or not request.app.config.get('TESTING'):
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        request.session = session
