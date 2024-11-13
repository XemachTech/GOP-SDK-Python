from urllib.parse import urljoin
from util.IopHashMap import IopHashMap
from api.GopExecutor import GopExecutor
from util.WebUtils import WebUtils


class GopRestExecutor(GopExecutor):
    def __init__(self, server_url, app_key, app_secret):
        super().__init__(server_url, app_key, app_secret)

    def getUrl(self, request, request_context):
        path = request.get_api_name()
        path_params = IopHashMap()
        sb = []
        api_params = request.get_api_params()
        arr = path.split("/")
        for s in arr:
            if not s:
                continue
            if s.startswith("{") and s.endswith("}"):
                k = s[1:-1]
                v = api_params.get(k)
                path_params[k] = v
                sb.append(f"/{v}")
            else:
                sb.append(f"/{s}")
        request_context.set_path_params(path_params)
        real_path = "".join(sb)
        request_context.set_api_name(real_path)
        return WebUtils.build_rest_url(f"{self.server_url}/rest/2.0", real_path)

    def getBizParams(self, request, request_context):
        path_params = request_context.get_path_params()
        biz_params = IopHashMap(
            request.get_api_params() if request.get_api_params() else {}
        )
        if not path_params:
            return biz_params
        result = IopHashMap()
        for key, value in biz_params.items():
            if key not in path_params:
                result[key] = value
        return result
