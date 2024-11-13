from datetime import datetime
from typing import Dict, Any
from api.IopRequest import IopRequest
from util.ApiException import ApiException
from util.WebUtils import WebUtils
from util.Constants import Constants
from util.IopUtils import IopUtils
from api.BaseExecutor import BaseExecutor
from util.RequestContext import RequestContext
import time


class GopExecutor(BaseExecutor):
    def __init__(self, server_url, app_key, app_secret):
        super().__init__(server_url, app_key, app_secret)

    def get_request_context(
        self, request: IopRequest, access_token: str, biz_params: Dict[str, Any]
    ) -> RequestContext:
        request_context = RequestContext()
        request_context.set_api_name(request.get_api_name())

        # add common parameters
        common_params = {}
        for key in request.get_api_params().keys():
            common_params[key] = request.get_api_params()[key]
        request_context.set_request_url(self.get_url(request, request_context))
        request_context.set_query_params(self.get_biz_params(request, request_context))
        common_params[Constants.APP_KEY] = self.app_key
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        timestamp_ms = str(
            int(datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").timestamp() * 1000)
        )

        common_params[Constants.TIMESTAMP] = (
            timestamp_ms  # datetime.fromtimestamp(timestamp / 1000)
        )
        common_params[Constants.SIGN_METHOD] = self.sign_method
        # common_params[Constants.METHOD] = self.g
        if access_token != "":
            common_params[Constants.ACCESS_TOKEN] = access_token
        common_params[Constants.PARTNER_ID] = self.sdk_version

        if self.is_debug_enabled():
            common_params[Constants.DEBUG] = True

        request_context.set_common_params(common_params)
        try:
            common_params[Constants.SIGN] = IopUtils.sign_api_request(
                request_context, self.app_secret, self.sign_method
            )
        except Exception as e:
            raise ApiException(e)

        return request_context

    def response_type(self) -> str:
        return Constants.RESPONSE_TYPE_DEFAULT

    def get_url(self, request: IopRequest, request_context: RequestContext) -> str:
        return WebUtils.build_rest_url(
            self.server_url + "/rest", request.get_api_name()
        )

    def get_biz_params(
        self, request: IopRequest, request_context: RequestContext
    ) -> Dict[str, Any]:
        return request.get_api_params() if request.get_api_params() else {}


# Example usage:
# gop_executor = GopExecutor("https://example.com", "app_key", "app_secret")
# request = IopRequest("api_name")
# context = gop_executor.get_request_context(request, "access_token", {})
