from typing import Type
from infra.parser.json.SimplifyJsonConverter import SimplifyJsonConverter
from util.ApiException import ApiException
from infra.mapping.GopParser import GopParser
from infra.parser.json.JsonConverter import JsonConverter

from typing import Type, TypeVar

T = TypeVar("T")


class ObjectJsonParser(GopParser):
    def __init__(self, clazz: Type[T], simplify: bool = False):
        self.clazz = clazz
        self.simplify = simplify

    def parse(self, rsp: str, response_type: str) -> T:
        if self.simplify:
            converter = SimplifyJsonConverter(response_type)
        else:
            converter = JsonConverter(response_type)
        return converter.to_response(rsp, self.clazz)

    def get_response_class(self) -> Type[T]:
        return self.clazz
