from abc import ABC, abstractmethod
from api.IopRequest import IopRequest


class BaseGopRequest(IopRequest, ABC):
    @abstractmethod
    def get_response_class(self):
        pass

    @abstractmethod
    def get_http_method(self):
        pass
