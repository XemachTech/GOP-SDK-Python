from datetime import datetime


class IopHashMap(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def put(self, key, value):
        if value is None:
            str_value = None
        elif isinstance(value, (str, int, float, bool)):
            str_value = str(value)
        elif isinstance(value, datetime):
            str_value = str(int(value.timestamp() * 1000))
        else:
            str_value = str(value)

        return self._put(key, str_value)

    def _put(self, key, value):
        if self.are_not_empty(key, value):
            self[key] = value
            return value
        else:
            return None

    @staticmethod
    def are_not_empty(*args):
        return all(arg is not None and arg != "" for arg in args)


# Utility function to mimic IopUtils.areNotEmpty
def are_not_empty(*args):
    return all(arg is not None and arg != "" for arg in args)


# # Example usage
# iop_map = IopHashMap()
# iop_map.put("key1", "value1")
# iop_map.put("key2", 123)
# iop_map.put("key3", 45.67)
# iop_map.put("key4", True)
# iop_map.put("key5", datetime.now())

# print(iop_map)
