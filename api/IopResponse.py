from typing import Dict, Optional


class IopResponse:
    def __init__(self):
        self.gop_error_type: Optional[str] = None
        self.gop_error_code: Optional[str] = None
        self.gop_error_message: Optional[str] = None
        self.gop_error_sub_code: Optional[str] = None
        self.gop_error_sub_msg: Optional[str] = None
        self.gop_request_id: Optional[str] = None
        self.gop_response_body: Optional[str] = None
        self.gop_request_params: Optional[Dict[str, str]] = None
        self.gop_request_url: Optional[str] = None

    def get_gop_request_params(self) -> Optional[Dict[str, str]]:
        return self.gop_request_params

    def set_gop_request_params(self, gop_request_params: Dict[str, str]) -> None:
        self.gop_request_params = gop_request_params

    def get_gop_request_url(self) -> Optional[str]:
        return self.gop_request_url

    def set_gop_request_url(self, gop_request_url: str) -> None:
        self.gop_request_url = gop_request_url

    def get_gop_error_sub_code(self) -> Optional[str]:
        return self.gop_error_sub_code

    def set_gop_error_sub_code(self, gop_error_sub_code: str) -> None:
        self.gop_error_sub_code = gop_error_sub_code

    def get_gop_error_sub_msg(self) -> Optional[str]:
        return self.gop_error_sub_msg

    def set_gop_error_sub_msg(self, gop_error_sub_msg: str) -> None:
        self.gop_error_sub_msg = gop_error_sub_msg

    def get_gop_error_type(self) -> Optional[str]:
        return self.gop_error_type

    def set_gop_error_type(self, gop_error_type: str) -> None:
        self.gop_error_type = gop_error_type

    def get_gop_error_code(self) -> Optional[str]:
        return self.gop_error_code

    def set_gop_error_code(self, gop_error_code: str) -> None:
        self.gop_error_code = gop_error_code

    def get_gop_error_message(self) -> Optional[str]:
        return self.gop_error_message

    def set_gop_error_message(self, gop_error_message: str) -> None:
        self.gop_error_message = gop_error_message

    def get_gop_request_id(self) -> Optional[str]:
        return self.gop_request_id

    def set_gop_request_id(self, gop_request_id: str) -> None:
        self.gop_request_id = gop_request_id

    def get_gop_response_body(self) -> Optional[str]:
        return self.gop_response_body

    def set_gop_response_body(self, gop_response_body: str) -> None:
        self.gop_response_body = gop_response_body

    def is_success(self) -> bool:
        return (
            self.gop_error_code is None
            or self.gop_error_code == ""
            or self.gop_error_code == "0"
        )
