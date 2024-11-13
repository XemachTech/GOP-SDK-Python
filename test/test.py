from api.IopClientImpl import IopClientImpl
from api.IopRequest import IopRequest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse, parse_qs
import time
from util.IopUtils import IopUtils
from api.GopExecutor import GopExecutor
from datetime import datetime
from util.WebUtils import WebUtils
from util.Constants import Constants
import json


def main():
    appkey = ""
    appSecret = ""
    access_token = ""

    client = IopClientImpl(
        "https://open-api.alibaba.com", appkey, appSecret
    )
    request = IopRequest()
    request.set_api_name("alibaba.icbu.product.schema.render")
    request.add_api_parameter(
        "param_product_top_publish_request",
        '{"product_id":"1601246789239","cat_id":"132612","language":"en_US"}',
    )
    response = client.execute(request, access_token)
    print(response.get_gop_response_body())

    return 0

    # client = IopClientImpl("http://open-api.alibaba.com", appkey, appSecret)
    # request = IopRequest()
    # request.set_api_name("/auth/token/create")
    # request.set_http_method(Constants.METHOD_GET)
    # request.add_api_parameter("code", "3_500088_ti8drHWLGDRt9AoUYBaE9ZSt4")
    # request.add_api_parameter("simplify", "true")
    # response = client.execute(request)
    # print(response)
    # data = json.loads(response.get_gop_response_body())
    # print(data)
    # access_token = data["access_token"]
    # print(access_token)
    # # print(response.body)
    # return 0


if __name__ == "__main__":
    main()
