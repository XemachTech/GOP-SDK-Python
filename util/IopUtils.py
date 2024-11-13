import hashlib
import hmac
import socket
from datetime import datetime


class IopUtils:
    intranet_ip = None

    @staticmethod
    def sign_api_request(request_context, app_secret, sign_method):
        """Sign the API request using particular method."""
        return IopUtils.sign_api_request_with_body(
            request_context.get_api_name(),
            request_context.get_all_params(),
            None,
            app_secret,
            sign_method,
        )

    @staticmethod
    def sign_api_request_with_body(api_name, params, body, app_secret, sign_method):
        """Sign the API request with body."""
        # Sort all text parameters
        sorted_keys = sorted(params.keys())

        # Connect all text parameters with key and value
        # query = api_name
        # for key in params.keys():
        #     value = params.get(key)
        #     if isinstance(value, datetime):
        #         value = str(int(value.timestamp() * 1000))
        #     if IopUtils.are_not_empty(key, value):
        #         query += key + value

        query = api_name
        for key in sorted_keys:
            value = params.get(key)
            if key and value:  # equivalent to Java's `areNotEmpty`
                query += key + value

        # Put the body at the end if present
        if body:
            query += body

        # Sign the request
        if sign_method in ["sha256", "hmac_sha256"]:
            # print("====IopUtils.encrypt_hmac_sha256")
            bytes_signature = IopUtils.encrypt_hmac_sha256(query, app_secret)
        else:
            raise IOError("Invalid Sign Method")

        # Convert sign result to uppercase hex string
        return bytes_signature.hex().upper()
        return IopUtils.byte_to_hex(bytes_signature).upper()

    # def sign_api_request(api_name, params, app_secret):
    # # first: sort all text parameters
    # print(api_name)
    # print(params)
    # sorted_keys = sorted(params.keys())

    # # second: connect all text parameters with key and value
    # query = api_name
    # for key in sorted_keys:
    #     value = params.get(key)
    #     if key and value:  # equivalent to Java's `areNotEmpty`
    #         query += key + value

    # bytes_signature = encrypt_hmac_sha256(query, app_secret)

    # # finally: transfer sign result from binary to upper hex string
    # return bytes_signature.hex().upper()

    @staticmethod
    def encrypt_hmac_sha256(data, secret):
        """Encrypt data using HMAC-SHA256."""
        return hmac.new(
            secret.encode("utf-8"), data.encode("utf-8"), hashlib.sha256
        ).digest()

    @staticmethod
    def byte_to_hex(byte_array):
        """Convert binary array to HEX string."""
        return "".join(f"{byte:02X}" for byte in byte_array)

    @staticmethod
    def cleanup_map(data_map):
        """Clean empty key or value items in map."""
        if not data_map:
            return None
        return {k: v for k, v in data_map.items() if v is not None}

    @staticmethod
    def get_intranet_ip():
        """Get local IP address. Return 127.0.0.1 on any exception."""
        if IopUtils.intranet_ip is None:
            try:
                IopUtils.intranet_ip = socket.gethostbyname(socket.gethostname())
            except Exception:
                IopUtils.intranet_ip = "127.0.0.1"
        return IopUtils.intranet_ip

    @staticmethod
    def is_empty(value):
        # print(value)
        """Check if a string is null or blank."""
        if isinstance(value, datetime):
            value = str(int(value.timestamp() * 1000))
        return value is None or not value.strip()

    @staticmethod
    def are_not_empty(*values):
        """Check if all given strings are not null or blank."""
        return all(value and not IopUtils.is_empty(value) for value in values)

    @staticmethod
    def format_date_time(date, pattern):
        """Format date using target pattern."""
        return datetime.strftime(date, pattern)
