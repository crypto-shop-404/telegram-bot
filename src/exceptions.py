__all__ = ('SendMailError',)


class SendMailError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
