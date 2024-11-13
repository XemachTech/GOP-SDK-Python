from abc import ABC, abstractmethod
from typing import Any, List, Type
from util.ApiException import ApiException


class Reader(ABC):
    """
    Interface for Reader
    """

    @abstractmethod
    def has_return_field(self, name: Any) -> bool:
        """
        Check if the response contains the specified field.

        :param name: Field name
        :return: True if field is present, False otherwise
        """
        pass

    @abstractmethod
    def get_primitive_object(self, name: Any) -> Any:
        """
        Read a single primitive object.

        :param name: Mapping name
        :return: Value of the primitive object
        """
        pass

    @abstractmethod
    def get_object(self, name: Any, type_class: Type) -> Any:
        """
        Read a single custom object.

        :param name: Mapping name
        :param type_class: Type of the mapping
        :return: Instance of the mapping type
        :raises ApiException: If an error occurs
        """
        pass

    @abstractmethod
    def get_list_objects(
        self, list_name: Any, item_name: Any, sub_type: Type
    ) -> List[Any]:
        """
        Read values of multiple objects.

        :param list_name: Name of the list
        :param item_name: Mapping name
        :param sub_type: Nested mapping type
        :return: List of instances of the nested mapping type
        :raises ApiException: If an error occurs
        """
        pass
