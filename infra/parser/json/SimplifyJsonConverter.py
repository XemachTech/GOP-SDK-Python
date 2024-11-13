from typing import Type, Dict, List, Any
from infra.mapping.Converter import Converter
from infra.mapping.Converters import Converters
from infra.mapping.Reader import Reader
from util.ApiException import ApiException
from util.Constants import Constants
from util.json.JSONReader import JSONReader
from util.json.JSONValidatingReader import JSONValidatingReader
from util.json.ExceptionErrorListener import ExceptionErrorListener

from typing import Type, TypeVar

T = TypeVar("T")


class SimplifyJsonConverter(Converter):
    def __init__(self, response_type: str):
        self.response_type = response_type

    def to_response(self, rsp: str, clazz: Type[T]) -> T:
        reader = JSONValidatingReader(ExceptionErrorListener())
        root_obj = reader.read(rsp)
        if isinstance(root_obj, dict):
            root_json = root_obj
            if self.response_type == Constants.RESPONSE_TYPE_DEFAULT:
                return self.from_json(root_json, clazz)
            else:
                error_json = root_json.get(Constants.RSP_ERR_RSP)
                if isinstance(error_json, dict):
                    return self.from_json(error_json, clazz)
                else:
                    return self.from_json(root_json, clazz)
        return None

    def from_json(self, json: Dict[Any, Any], clazz: Type[T]) -> T:
        return Converters.convert(clazz, Reader(json))

    def get_response_type(self) -> str:
        return self.response_type

    def set_response_type(self, response_type: str):
        self.response_type = response_type


class Reader:
    def __init__(self, json: Dict[Any, Any]):
        self.json = json

    def has_return_field(self, name: Any) -> bool:
        return name in self.json

    def get_primitive_object(self, name: Any) -> Any:
        return self.json.get(name)

    def get_object(self, name: Any, obj_type: Type) -> Any:
        tmp = self.json.get(name)
        if isinstance(tmp, dict):
            return SimplifyJsonConverter.from_json(tmp, obj_type)
        else:
            return tmp

    def get_list_objects(
        self, list_name: Any, item_name: Any, sub_type: Type
    ) -> List[Any]:
        list_objs = []
        json_list = self.json.get(list_name)
        if isinstance(json_list, list):
            for tmp in json_list:
                if isinstance(tmp, dict):
                    list_objs.append(SimplifyJsonConverter.from_json(tmp, sub_type))
                elif isinstance(tmp, list):
                    # TODO not supported yet
                    pass
                else:
                    list_objs.append(tmp)
        return list_objs
