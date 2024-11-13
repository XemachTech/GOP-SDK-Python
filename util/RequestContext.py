class RequestContext:
    def __init__(self):
        self.start = None
        self.request_url = None
        self.response_body = None
        self.api_name = None
        self.common_params = {}
        self.query_params = {}
        self.path_params = {}

    def get_start(self):
        return self.start

    def set_start(self, start):
        self.start = start

    def get_path_params(self):
        return self.path_params

    def set_path_params(self, path_params):
        self.path_params = path_params

    def get_request_url(self):
        return self.request_url

    def set_request_url(self, request_url):
        self.request_url = request_url

    def get_response_body(self):
        return self.response_body

    def set_response_body(self, response_body):
        self.response_body = response_body

    def get_query_params(self):
        return self.query_params

    def set_query_params(self, query_params):
        self.query_params = query_params

    def get_api_name(self):
        return self.api_name

    def set_api_name(self, api_name):
        self.api_name = api_name

    def get_common_params(self):
        return self.common_params

    def set_common_params(self, common_params):
        self.common_params = common_params

    def get_all_params(self):
        params = {}
        if self.common_params:
            params.update(self.common_params)
        if self.query_params:
            params.update(self.query_params)
        return params
