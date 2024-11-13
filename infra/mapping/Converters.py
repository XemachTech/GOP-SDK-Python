from api.IopResponse import IopResponse
from util.ApiException import ApiException
from util.Constants import Constants
from util.StringUtils import StringUtils
from util.json.JSONWriter import JSONWriter

from datetime import datetime
from typing import Any, List, Type, Set, Dict
from collections import defaultdict


isCheckJsonType = False


class Converters:
    emptyCache = object()
    baseProps: Dict[str, Set[str]] = defaultdict(set)
    fieldCache: Dict[str, Any] = {}
    methodCache: Dict[str, Any] = {}

    baseProps[IopResponse.__name__] = StringUtils.get_class_properties(
        IopResponse, False
    )

    @staticmethod
    def convert(clazz: Type, reader: Any) -> Any:
        rsp = clazz()

        try:
            successField = None
            successFields = [
                field
                for field in dir(clazz)
                if not callable(getattr(clazz, field)) and not field.startswith("__")
            ]
            for field in successFields:
                if field == "success":
                    successField = field

            successMethod = None
            methods = [
                method for method in dir(clazz) if callable(getattr(clazz, method))
            ]
            for method in methods:
                if method == "setSuccess":
                    successMethod = getattr(clazz, method)

            if successField and successMethod:
                successItemName = successField
                successListName = None
                jsonField = getattr(clazz, successField).__annotations__.get("ApiField")
                if jsonField:
                    successItemName = jsonField.value()
                jsonListField = getattr(clazz, successField).__annotations__.get(
                    "ApiListField"
                )
                if jsonListField:
                    successListName = jsonListField.value()

                if not reader.hasReturnField(successItemName):
                    if not successListName or not reader.hasReturnField(
                        successListName
                    ):
                        pass

                Converters.setMethodValue(
                    rsp,
                    reader,
                    successItemName,
                    successListName,
                    successField,
                    successMethod,
                )

            for prop in dir(clazz):
                if callable(getattr(clazz, prop)) or prop.startswith("__"):
                    continue

                field = getattr(clazz, prop, None)
                if field is None:
                    continue

                jsonField = field.__annotations__.get("ApiField")
                itemName = jsonField.value() if jsonField else prop
                jsonListField = field.__annotations__.get("ApiListField")
                listName = jsonListField.value() if jsonListField else None

                if not reader.hasReturnField(itemName) and (
                    not listName or not reader.hasReturnField(listName)
                ):
                    continue

                method = Converters.getCacheMethod(clazz, prop)
                if method:
                    Converters.setMethodValue(
                        rsp, reader, itemName, listName, field, method
                    )

        except Exception as e:
            raise ApiException(e)

        return rsp

    @staticmethod
    def getField(clazz: Type, pd: str) -> Any:
        key = f"{clazz.__name__}_{pd}"
        field = Converters.fieldCache.get(key)
        if field is None:
            try:
                field = getattr(clazz, pd)
            except AttributeError:
                field = Converters.emptyCache
            Converters.fieldCache[key] = field
        return None if field == Converters.emptyCache else field

    @staticmethod
    def getCacheMethod(clazz: Type, pd: str) -> Any:
        key = f"{clazz.__name__}_{pd}"
        method = Converters.methodCache.get(key)
        if method is None:
            method = getattr(clazz, pd, Converters.emptyCache)
            Converters.methodCache[key] = method
        return None if method == Converters.emptyCache else method

    @staticmethod
    def setMethodValue(
        rsp: Any, reader: Any, itemName: str, listName: str, field: str, method: Any
    ) -> None:
        typeClass = type(getattr(rsp, field, None))

        if typeClass == str:
            value = reader.get_primitive_object(itemName)
            if isinstance(value, str):
                method(rsp, value)
            elif isinstance(value, dict):
                method(rsp, JSONWriter().write(value))
            elif value is not None:
                method(rsp, str(value))
            else:
                method(rsp, "")

        elif typeClass == int:
            value = reader.get_primitive_object(itemName)
            if isinstance(value, int):
                method(rsp, value)

        elif typeClass == bool:
            value = reader.get_primitive_object(itemName)
            if isinstance(value, bool):
                method(rsp, value)

        elif typeClass == datetime:
            value = reader.get_primitive_object(itemName)
            if isinstance(value, str):
                method(rsp, StringUtils.parse_date_time(value))
            elif isinstance(value, int):
                method(rsp, datetime.fromtimestamp(value / 1000))

        elif typeClass == list:
            # Process List types with potential generics (inferred)
            pass

        # Add other types as necessary based on field type handling requirements
