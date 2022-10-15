__all__ = ('SendMailError', 'UserNotInDatabase')


class SendMailError(Exception):
    pass


class UserNotInDatabase(Exception):
    pass
