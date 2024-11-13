import datetime
import logging
import platform
import urllib.parse


class IopLogger:
    LOG_SPLIT = "^_^"
    os_name = platform.system()
    need_enable_logger = True

    @staticmethod
    def set_need_enable_logger(need_enable_logger):
        IopLogger.need_enable_logger = need_enable_logger

    @staticmethod
    def write(app_key, sdk_version, api_name, url, params, latency, error_message):
        if not IopLogger.need_enable_logger:
            return

        log_message = IopLogger.build_log_api(
            app_key, sdk_version, api_name, url, params, latency, error_message
        )
        logging.error(log_message)

    @staticmethod
    def build_log_api(
        app_key, sdk_version, api_name, url, params, latency, error_message
    ):
        log_parts = [
            IopLogger.format_date_time(datetime.datetime.now()),  # timestamp
            app_key,  # appkey
            sdk_version,
            api_name,
            IopUtils.get_intranet_ip(),  # internal ip address
            IopLogger.os_name,
            str(latency),
            url,  # gateway URL
        ]
        try:
            log_parts.append(
                urllib.parse.urlencode(params, encoding="utf-8")
            )  # parameters
        except Exception as e:
            pass
        log_parts.append(error_message)  # error info
        return IopLogger.LOG_SPLIT.join(log_parts)

    @staticmethod
    def format_date_time(date):
        return IopUtils.format_date_time(date, "%Y-%m-%d %H:%M:%S.%f")


class IopUtils:
    @staticmethod
    def get_intranet_ip():
        # This method should be implemented to return the intranet IP address
        pass

    @staticmethod
    def format_date_time(date, format_str):
        return date.strftime(format_str)


# Configure logging
logging.basicConfig(level=logging.ERROR)
