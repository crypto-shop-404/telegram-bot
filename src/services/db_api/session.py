import contextlib
import typing

import sqlalchemy.orm
from sqlalchemy import orm

from services.db_api import engine


RawSession = sqlalchemy.orm.sessionmaker(bind=engine.engine)


@contextlib.contextmanager
def create_session() -> typing.Generator[orm.Session, None, None]:
    with RawSession() as session, session.begin():
        yield session
