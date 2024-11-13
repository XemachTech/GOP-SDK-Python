from datetime import datetime
from collections import defaultdict

from util.IopHashMap import IopHashMap
from util.Constants import Constants
from api.IopResponse import IopResponse


class IopRequest:
    def __init__(self, api_name=None):
        self.api_params = None
        self.header_params = None
        self.file_params = None
        self.timestamp = None
        self.api_name = api_name
        self.http_method = Constants.METHOD_POST

    def add_api_parameter(self, key, value):
        if self.api_params is None:
            self.api_params = IopHashMap()
        self.api_params[key] = value

    def add_file_parameter(self, key, file):
        if self.file_params is None:
            self.file_params = {}
        self.file_params[key] = file

    def add_header_parameter(self, key, value):
        if self.header_params is None:
            self.header_params = IopHashMap()
        self.header_params[key] = value

    def get_api_params(self):
        return self.api_params

    def get_file_params(self):
        return self.file_params

    def get_header_params(self):
        return self.header_params

    def get_timestamp(self):
        return self.timestamp

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def get_api_name(self):
        return self.api_name

    def set_api_name(self, api_name):
        self.api_name = api_name

    def get_http_method(self):
        return self.http_method

    def set_http_method(self, http_method):
        self.http_method = http_method

    def set_header_params(self, header_params):
        self.header_params = header_params

    def get_response_class(self):
        return IopResponse().__class__
