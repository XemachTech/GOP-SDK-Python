import json
import time
import requests
from abc import ABC, abstractmethod
from infra.parser.json.ObjectJsonParser import ObjectJsonParser
from infra.parser.xml.ObjectXmlParser import ObjectXmlParser
from util.IopLogger import IopLogger
from util.ApiException import ApiException
from urllib.parse import quote


class BaseExecutor(ABC):

    def __init__(self, server_url, app_key, app_secret):
        self.server_url = server_url.rstrip("/")
        self.app_key = app_key
        self.app_secret = app_secret

        self.sign_method = "sha256"  # Constants.SIGN_METHOD_SHA256
        self.connect_timeout = 15  # default connection timeout in seconds
        self.read_timeout = 30  # default read timeout in seconds
        self.use_gzip_encoding = True  # use gzip encoding or not
        self.proxy = None
        self.sdk_version = "iop-sdk-python-20181207"
        self.log_level = "ERROR"  # Constants.LOG_LEVEL_ERROR
        self.format = "JSON"  # Constants.FORMAT_JSON
        self.need_parser = True
        self.simplify = True

    @abstractmethod
    def get_request_context(self, request, access_token, biz_params):
        pass

    def build_parser(self, response_class):
        if self.format == "JSON":
            return ObjectJsonParser(response_class, self.simplify)
        else:
            return ObjectXmlParser(response_class)

    def do_execute(self, request, access_token):
        parser = self.build_parser(request.get_response_class())
        context = self.invoke(request, access_token)
        t_rsp = self.parse_body(parser, request, context)

        t_rsp.set_gop_request_params(context.get_all_params())
        if not t_rsp.is_success():
            IopLogger.write(
                self.app_key,
                self.sdk_version,
                request.get_api_name(),
                self.server_url,
                context.get_all_params(),
                time.time() - context.get_start(),
                t_rsp.get_gop_response_body(),
            )
        return t_rsp

    def parse_body(self, parser, request, request_context):
        body = request_context.get_response_body()
        t_rsp = None
        if self.need_parser:
            t_rsp = parser.parse(body, self.response_type())
            if t_rsp is None:
                try:
                    t_rsp = request.get_response_class()()
                except Exception as e:
                    raise ApiException(e)
            t_rsp.set_gop_response_body(body)
            t_rsp.set_gop_request_url(request_context.get_request_url())
        else:
            try:
                t_rsp = request.get_response_class()()
                t_rsp.set_gop_response_body(body)
                t_rsp.set_gop_request_url(request_context.get_request_url())
            except Exception as e:
                raise ApiException(e)
        return t_rsp

    def invoke(self, request, access_token):
        start = time.time()

        biz_params = request.get_api_params() or {}

        request_context = self.get_request_context(request, access_token, biz_params)
        request_context.set_start(start)
        try:
            rpc_url = request_context.get_request_url()
            url_query = self.build_query(request_context.get_common_params())
            full_url = self.build_request_url(rpc_url, url_query)
            # print("full_url:" + full_url)
            full_url = quote(full_url, safe=":/?=&")
            # print("new full_url:" + full_url)
            request_context.set_request_url(full_url)
            headers = request.get_header_params() or {}

            if self.use_gzip_encoding:
                headers["Accept-Encoding"] = "gzip"

            if request.get_file_params():
                response = requests.post(
                    full_url,
                    data=biz_params,
                    files=request.get_file_params(),
                    headers=headers,
                    timeout=(self.connect_timeout, self.read_timeout),
                    proxies=self.proxy,
                )
            else:
                if request.get_http_method() == "POST":
                    response = requests.post(
                        full_url,
                        data=biz_params,
                        headers=headers,
                        timeout=(self.connect_timeout, self.read_timeout),
                        proxies=self.proxy,
                    )
                else:
                    headers = {
                        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                        "Accept-Encoding": "gzip",
                    }
                    response = requests.get(
                        full_url,
                        params=biz_params,
                        headers=headers,
                        timeout=(self.connect_timeout, self.read_timeout),
                        proxies=self.proxy,
                    )
            request_context.set_response_body(response.text)
        except requests.RequestException as e:
            IopLogger.write(
                self.app_key,
                self.sdk_version,
                request.get_api_name(),
                self.server_url,
                request_context.get_all_params(),
                time.time() - start,
                str(e),
            )
            raise ApiException(e)
        return request_context

    def build_query(self, params):
        params = dict(sorted(params.items()))
        return "&".join([f"{k}={v}" for k, v in params.items()])

    def build_request_url(self, base_url, query):
        return f"{base_url}?{query}"

    def is_debug_enabled(self):
        return self.log_level == "DEBUG"

    def is_info_enabled(self):
        return self.log_level == "INFO"

    def is_error_enabled(self):
        return self.log_level == "ERROR"

    def get_connect_timeout(self):
        return self.connect_timeout

    def set_connect_timeout(self, connect_timeout):
        self.connect_timeout = connect_timeout

    def get_read_timeout(self):
        return self.read_timeout

    def set_read_timeout(self, read_timeout):
        self.read_timeout = read_timeout

    def is_use_gzip_encoding(self):
        return self.use_gzip_encoding

    def set_use_gzip_encoding(self, use_gzip_encoding):
        self.use_gzip_encoding = use_gzip_encoding

    def get_sign_method(self):
        return self.sign_method

    def set_sign_method(self, sign_method):
        self.sign_method = sign_method

    def get_proxy(self):
        return self.proxy

    def set_proxy(self, proxy):
        self.proxy = proxy

    def get_log_level(self):
        return self.log_level

    def set_log_level(self, log_level):
        self.log_level = log_level

    @abstractmethod
    def response_type(self):
        pass
