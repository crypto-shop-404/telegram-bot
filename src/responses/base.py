import abc


class BaseResponse(abc.ABC):

    def __await__(self):
        return self._send_response().__await__()

    @abc.abstractmethod
    async def _send_response(self):
        pass
