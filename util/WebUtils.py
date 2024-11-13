import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urlencode, urljoin
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from io import BytesIO
import gzip


class WebUtils:
    DEFAULT_CHARSET = "utf-8"
    ignore_ssl_check = True
    ignore_host_check = True

    @staticmethod
    def set_ignore_ssl_check(ignore_ssl_check):
        WebUtils.ignore_ssl_check = ignore_ssl_check

    @staticmethod
    def set_ignore_host_check(ignore_host_check):
        WebUtils.ignore_host_check = ignore_host_check

    @staticmethod
    def do_get(url, params, connect_timeout, read_timeout):
        return WebUtils.request(
            url,
            params,
            None,
            connect_timeout,
            read_timeout,
            WebUtils.DEFAULT_CHARSET,
            None,
            "GET",
        )

    @staticmethod
    def request(
        url,
        query_params,
        header_params,
        connect_timeout,
        read_timeout,
        charset,
        proxy,
        method,
    ):
        try:
            query = WebUtils.build_query(query_params, charset)
            full_url = WebUtils.build_get_url(url, query)
            response = requests.request(
                method,
                full_url,
                headers=header_params,
                timeout=(connect_timeout, read_timeout),
                proxies=proxy,
                verify=not WebUtils.ignore_ssl_check,
            )
            return WebUtils.get_response_as_string(response)
        except Exception as e:
            raise IOError(str(e))

    @staticmethod
    def do_post(url, params, connect_timeout, read_timeout):
        return WebUtils.do_post_with_body(
            url,
            params,
            None,
            WebUtils.DEFAULT_CHARSET,
            connect_timeout,
            read_timeout,
            None,
        )

    @staticmethod
    def do_post_with_body(url, body, headers, charset, connect_timeout, read_timeout):
        try:
            headers = headers or {}
            headers["Content-Type"] = f"text/plain;charset={charset}"
            response = requests.post(
                url,
                data=body.encode(charset),
                headers=headers,
                timeout=(connect_timeout, read_timeout),
                verify=not WebUtils.ignore_ssl_check,
            )
            return WebUtils.get_response_as_string(response)
        except Exception as e:
            raise IOError(str(e))

    @staticmethod
    def do_post_with_files(
        url,
        query_params,
        file_params,
        header_params,
        charset,
        connect_timeout,
        read_timeout,
    ):
        try:
            files = {
                key: (
                    file_item["filename"],
                    file_item["content"],
                    file_item["mimetype"],
                )
                for key, file_item in file_params.items()
            }
            response = requests.post(
                url,
                data=query_params,
                files=files,
                headers=header_params,
                timeout=(connect_timeout, read_timeout),
                verify=not WebUtils.ignore_ssl_check,
            )
            return WebUtils.get_response_as_string(response)
        except Exception as e:
            raise IOError(str(e))

    @staticmethod
    def build_query(params, charset):
        if not params:
            return None
        return urlencode(params, encoding=charset)

    @staticmethod
    def is_empty(value: str) -> bool:
        return value is None or value.strip() == ""

    @staticmethod
    def build_request_url(url: str, *queries: str) -> str:
        if not queries:
            return url

        new_url = [url]
        has_query = "?" in url
        has_prepend = url.endswith("?") or url.endswith("&")

        for query in queries:
            if not WebUtils.is_empty(query):
                if not has_prepend:
                    if has_query:
                        new_url.append("&")
                    else:
                        new_url.append("?")
                        has_query = True
                new_url.append(query)
                has_prepend = False

        return "".join(new_url)

    @staticmethod
    def build_rest_url(url: str, api_name: str) -> str:
        print("======")
        if not api_name:
            return url

        has_prepend = url.endswith("/")
        if has_prepend:
            return url + api_name[1:]
        else:
            return url + api_name

    @staticmethod
    def build_get_url(url, query):
        if not query:
            return url
        return f"{url}?{query}"

    @staticmethod
    def get_response_as_string(response):
        if response.status_code < 400:
            if "gzip" in response.headers.get("Content-Encoding", ""):
                buf = BytesIO(response.content)
                f = gzip.GzipFile(fileobj=buf)
                return f.read().decode(response.encoding or WebUtils.DEFAULT_CHARSET)
            return response.text
        else:
            raise IOError(f"{response.status_code} {response.reason}")


# Example usage
# url = 'http://example.com/api'
# params = {'key1': 'value1', 'key2': 'value2'}
# connect_timeout = 10
# read_timeout = 30
# response = WebUtils.do_get(url, params, connect_timeout, read_timeout)
# print(response)
