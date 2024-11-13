import time
from datetime import datetime
from util.IopHashMap import IopHashMap
from util.ApiException import ApiException
from util.IopUtils import IopUtils
from api.BaseExecutor import BaseExecutor
from util.RequestContext import RequestContext
from util.Constants import Constants
from util.StringUtils import StringUtils


class TopExecutor(BaseExecutor):
    def __init__(self, server_url, app_key, app_secret):
        super().__init__(server_url, app_key, app_secret)

    def get_request_context(self, request, access_token, biz_params):
        request_context = RequestContext()
        request_context.set_api_name(request.get_api_name())

        params = request.get_api_params()
        common_params = IopHashMap()
        request_context.set_query_params(biz_params)
        common_params[Constants.APP_KEY] = self.app_key
        common_params[Constants.VERSION] = "2.0"
        timestamp = request.get_timestamp()
        if timestamp is None:
            timestamp = int(time.time() * 1000)

        common_params[Constants.TIMESTAMP] = datetime.fromtimestamp(timestamp / 1000)
        common_params[Constants.METHOD] = request.get_api_name()
        common_params[Constants.FORMAT] = self.format
        common_params[Constants.SESSION] = access_token
        common_params[Constants.PARTNER_ID] = self.sdk_version
        common_params[Constants.SIGN_METHOD] = self.sign_method
        if params is None:
            params = IopHashMap()
        simplify = params.get(Constants.SIMPLIFY)
        if StringUtils.is_empty(simplify):
            simplify = str(self.simplify)
        if simplify == str(True):
            common_params[Constants.SIMPLIFY] = str(True)

        if self.is_debug_enabled():
            common_params[Constants.DEBUG] = True

        request_context.set_common_params(common_params)
        request_context.set_request_url(
            f"{self.server_url}/sync?method={request.get_api_name()}"
        )
        try:
            common_params[Constants.SIGN] = IopUtils.sign_api_request_with_body(
                "",
                request_context.get_all_params(),
                None,
                self.app_secret,
                self.sign_method,
            )
        except Exception as e:
            print(e)
            raise ApiException(e)
        return request_context

    def response_type(self):
        return Constants.RESPONSE_TYPE_AE_DEFAULT
