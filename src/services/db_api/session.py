import contextlib

import sqlalchemy.orm

from services.db_api import engine


RawSession = sqlalchemy.orm.sessionmaker(bind=engine.engine)


@contextlib.contextmanager
def create_session():
    with RawSession() as session, session.begin():
        yield session
