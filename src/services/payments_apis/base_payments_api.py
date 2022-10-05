import abc


class BasePaymentAPI(abc.ABC):
    @abc.abstractmethod
    def check(self) -> bool:
        pass
