import collections
from enum import Enum
from typing import Dict, Type

from api.IopClient import IopClient
from api.GopExecutor import GopExecutor
from api.TopExecutor import TopExecutor
from api.GopRestExecutor import GopRestExecutor
from api.Protocol import Protocol
from util.IopLogger import IopLogger
from util.WebUtils import WebUtils
from api.BaseExecutor import BaseExecutor
from api.BaseGopRequest import BaseGopRequest
from api.IopRequest import IopRequest


class IopClientImpl(IopClient):
    def __init__(
        self,
        server_url: str,
        app_key: str,
        app_secret: str,
        connect_timeout: int = 15,
        read_timeout: int = 30,
    ):
        self.gop_delegate = GopExecutor(server_url, app_key, app_secret)
        self.top_delegate = TopExecutor(server_url, app_key, app_secret)
        self.gop_rest_delegate = GopRestExecutor(server_url, app_key, app_secret)
        self.factory: Dict[Protocol, BaseExecutor] = {
            Protocol.GOP: self.gop_delegate,
            Protocol.TOP: self.top_delegate,
            Protocol.REST_VND_2: self.gop_rest_delegate,
        }
        self.set_connect_timeout(connect_timeout)
        self.set_read_timeout(read_timeout)

    def execute(
        self,
        request: BaseGopRequest,
        access_token: str = "",
        protocol: Protocol = Protocol.GOP,
    ):
        return self.factory.get(protocol).do_execute(request, access_token)

    def execute_request(
        self,
        request: IopRequest,
        access_token: str = "",
        protocol: Protocol = Protocol.GOP,
    ):
        return self.factory.get(protocol).do_execute(request, access_token)

    def set_need_enable_logger(self, need_enable_logger):
        IopLogger.set_need_enable_logger(need_enable_logger)

    def set_ignore_ssl_check(self, ignore):
        WebUtils.set_ignore_ssl_check(ignore)

    def set_use_gzip_encoding(self, use_gzip_encoding: bool):
        for executor in self.factory.values():
            executor.set_use_gzip_encoding(use_gzip_encoding)

    def set_connect_timeout(self, connect_timeout: int):
        for executor in self.factory.values():
            executor.set_connect_timeout(connect_timeout)

    def set_read_timeout(self, read_timeout: int):
        for executor in self.factory.values():
            executor.set_read_timeout(read_timeout)

    def set_sign_method(self, sign_method: str):
        for executor in self.factory.values():
            executor.set_sign_method(sign_method)

    def set_proxy(self, proxy):
        for executor in self.factory.values():
            executor.set_proxy(proxy)

    def set_log_level(self, log_level: str):
        for executor in self.factory.values():
            executor.set_log_level(log_level)
