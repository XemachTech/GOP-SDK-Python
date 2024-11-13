from abc import ABC, abstractmethod
from typing import Type, TypeVar
from util.ApiException import ApiException

T = TypeVar("T")


class Converter(ABC):
    """
    Interface for converting a string to a response object.
    """

    @abstractmethod
    def to_response(self, rsp: str, clazz: Type[T]) -> T:
        """
        Convert a string response to a response object.

        :param rsp: The response string
        :param clazz: The class type of the domain
        :return: The response object
        :raises ApiException: if the conversion fails
        """
        pass
