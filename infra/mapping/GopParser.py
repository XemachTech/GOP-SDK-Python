from util.ApiException import ApiException

from abc import ABC, abstractmethod
from typing import Type, TypeVar

T = TypeVar("T")


class GopParser(ABC):
    """
    Python translation of Java GopParser interface.
    Translates response string to domain-specific object.

    Attributes:
        rsp (str): response string
        responseType (str): response format
    """

    @abstractmethod
    def parse(self, rsp: str, responseType: str) -> T:
        """
        Parse the response string into the domain object.

        Args:
            rsp (str): Response string
            responseType (str): Response format

        Returns:
            T: Domain object
        """
        raise ApiException("Method not implemented")

    @abstractmethod
    def get_response_class(self) -> Type[T]:
        """
        Get the response class type.

        Returns:
            Type[T]: The response class type
        """
        raise ApiException("Method not implemented")
