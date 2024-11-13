import json
import datetime
from collections import deque


class JSONWriter:
    def __init__(self, emit_class_name=False, use_api_style=False, use_api_field=True):
        self.buf = []
        self.calls = deque()
        self.emit_class_name = emit_class_name
        self.use_api_style = use_api_style
        self.use_api_field = use_api_field

    def write(self, obj):
        self.buf.clear()
        self.value(obj)
        return "".join(self.buf)

    def value(self, obj):
        if obj is None or self.cyclic(obj):
            self.add("null")
        else:
            self.calls.append(obj)
            if isinstance(obj, bool):
                self.add(json.dumps(obj))
            elif isinstance(obj, (int, float)):
                self.add(str(obj))
            elif isinstance(obj, str):
                self.string(obj)
            elif isinstance(obj, (list, tuple, set)):
                self.array(obj)
            elif isinstance(obj, dict):
                self.map(obj)
            elif isinstance(obj, datetime.date):
                self.date(obj)
            else:
                self.bean(obj)
            self.calls.pop()

    def cyclic(self, obj):
        return obj in self.calls

    def bean(self, obj):
        self.add("{")
        added_something = False
        for name, value in vars(obj).items():
            if value is not None:
                if added_something:
                    self.add(",")
                self.add_name_value(name, value)
                added_something = True
        self.add("}")

    def map(self, obj):
        self.add("{")
        added_something = False
        for key, value in obj.items():
            if added_something:
                self.add(",")
            self.value(key)
            self.add(":")
            self.value(value)
            added_something = True
        self.add("}")

    def array(self, obj):
        self.add("[")
        for i, item in enumerate(obj):
            if i > 0:
                self.add(",")
            self.value(item)
        self.add("]")

    def date(self, obj):
        self.add(f'"{obj.isoformat()}"')

    def string(self, obj):
        self.add(f'"{obj}"')

    def add_name_value(self, name, value):
        self.string(name)
        self.add(":")
        self.value(value)

    def add(self, content):
        self.buf.append(content)
