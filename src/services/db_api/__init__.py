from .session import create_session
from . import listeners

from services.db_api import engine
from services.db_api import base


def setup_database() -> None:
    base.Base.metadata.create_all(engine.engine)
