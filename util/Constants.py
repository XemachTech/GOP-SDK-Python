class Constants:
    """Constant values."""

    # Iop common request parameters
    APP_KEY = "app_key"
    TIMESTAMP = "timestamp"
    SIGN = "sign"
    SIGN_METHOD = "sign_method"
    ACCESS_TOKEN = "access_token"
    PARTNER_ID = "partner_id"
    DEBUG = "debug"
    NONCE = "nonce"

    # TOP
    FORMAT_JSON = "json"
    FORMAT = "format"
    METHOD = "method"
    VERSION = "v"
    SESSION = "session"
    SIMPLIFY = "simplify"
    TARGET_APP_KEY = "target_app_key"

    DATE_TIMEZONE = "GMT+8"
    RESPONSE_TYPE_AE_DEFAULT = "AE_DEFAULT"
    RESPONSE_TYPE_DEFAULT = "DEFAULT"

    # Iop error response parameters
    RSP_TYPE = "type"
    RSP_CODE = "code"
    RSP_MSG = "message"
    RSP_REQUEST_ID = "request_id"
    RSP_ERR_RSP = "error_response"

    DATE_TIME_FORMAT = "yyyy-MM-dd HH:mm:ss"

    CHARSET_UTF8 = "UTF-8"

    METHOD_POST = "POST"
    METHOD_GET = "GET"
    METHOD_PUT = "PUT"
    METHOD_DELETE = "DELETE"

    SIGN_METHOD_HMAC = "hmac"
    SIGN_METHOD_HMAC_MD5 = "HmacMD5"

    SIGN_METHOD_SHA256 = "sha256"
    SIGN_METHOD_HMAC_SHA256 = "HmacSHA256"

    SDK_VERSION = "iop-sdk-java"
    ACCEPT_ENCODING = "Accept-Encoding"
    CONTENT_ENCODING = "Content-Encoding"
    CONTENT_ENCODING_GZIP = "gzip"
    MIME_TYPE_DEFAULT = "application/octet-stream"

    READ_BUFFER_SIZE = 1024 * 4

    # iop log level
    LOG_LEVEL_DEBUG = "DEBUG"
    LOG_LEVEL_INFO = "INFO"
    LOG_LEVEL_ERROR = "ERROR"
