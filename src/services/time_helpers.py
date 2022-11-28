import datetime

__all__ = (
    'get_new_york_now',
)


def get_new_york_now() -> datetime.datetime:
    return datetime.datetime.utcnow() - datetime.timedelta(hours=5)
