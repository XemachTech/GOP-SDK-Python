from xml.etree import ElementTree as ET
from typing import Type, TypeVar
from util.ApiException import ApiException

T = TypeVar("T")


class Converter:
    def __init__(self, response_type: str):
        self.response_type = response_type

    def to_response(self, rsp: str, clazz: Type[T]) -> T:
        # Assuming the conversion logic is to parse the XML and create an instance of clazz
        try:
            root = ET.fromstring(rsp)
            # Here, you would convert the XML root to an instance of clazz
            # This is a placeholder for the actual conversion logic
            return clazz()  # This should be replaced with actual conversion logic
        except ET.ParseError as e:
            raise ApiException(f"Failed to parse XML: {e}")


class ObjectXmlParser:
    def __init__(self, clazz: Type[T]):
        self.clazz = clazz

    def parse(self, rsp: str, response_type: str) -> T:
        converter = Converter(response_type)
        return converter.to_response(rsp, self.clazz)

    def get_response_class(self) -> Type[T]:
        return self.clazz
