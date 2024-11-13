from api.BaseGopRequest import BaseGopRequest
from api.Protocol import Protocol
from api.IopResponse import IopResponse
from api.IopRequest import IopRequest
from enum import Enum
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T", bound="IopResponse")


class IopClient(ABC):

    @abstractmethod
    def execute(self, request: "BaseGopRequest[T]") -> T:
        """Execute API request without access token."""
        pass

    @abstractmethod
    def execute(self, request: "BaseGopRequest[T]", access_token: str) -> T:
        """Execute API request with access token."""
        pass

    @abstractmethod
    def execute(
        self, request: "BaseGopRequest[T]", access_token: str, protocol: "Protocol"
    ) -> T:
        """Execute API request with access token and protocol."""
        pass

    @abstractmethod
    def execute(self, request: "BaseGopRequest[T]", protocol: "Protocol") -> T:
        """Execute API request with protocol but without access token."""
        pass

    @abstractmethod
    def execute_request(self, request: "IopRequest") -> "IopResponse":
        """Execute a standard API request without access token."""
        pass

    @abstractmethod
    def execute_request(
        self, request: "IopRequest", access_token: str
    ) -> "IopResponse":
        """Execute a standard API request with access token."""
        pass

    @abstractmethod
    def execute_request(
        self, request: "IopRequest", protocol: "Protocol"
    ) -> "IopResponse":
        """Execute a standard API request with protocol but without access token."""
        pass

    @abstractmethod
    def execute_request(
        self, request: "IopRequest", access_token: str, protocol: "Protocol"
    ) -> "IopResponse":
        """Execute a standard API request with access token and protocol."""
        pass
