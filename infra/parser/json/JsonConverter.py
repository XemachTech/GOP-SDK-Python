from typing import Type, List, Dict, Any
import json

# Import your external modules, assuming they exist
from infra.mapping.Converter import Converter
from infra.mapping.Converters import Converters
from infra.mapping.Reader import Reader
from util.ApiException import ApiException
from util.json.ExceptionErrorListener import ExceptionErrorListener
from util.json.JSONValidatingReader import JSONValidatingReader

# JSONReader, JSONValidatingReader


class JsonConverter(Converter):

    def __init__(self, response_type: str):
        self.response_type = response_type

    def to_response(self, rsp: str, clazz: Type) -> Any:
        reader = JSONValidatingReader(ExceptionErrorListener())
        root_obj = reader.read(rsp)
        if isinstance(root_obj, dict):
            root_json = root_obj
            values = root_json.values()
            for rsp_obj in values:
                if isinstance(rsp_obj, dict):
                    rsp_json = rsp_obj
                    return self.from_json(rsp_json, clazz)
        return None

    def from_json(self, json_data: Dict, clazz: Type) -> Any:
        return Converters.convert(clazz, Reader(self, json_data))

    def get_response_type(self) -> str:
        return self.response_type

    def set_response_type(self, response_type: str) -> None:
        self.response_type = response_type
