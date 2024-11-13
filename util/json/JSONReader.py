from collections import deque
import re
from decimal import Decimal
from typing import Any, Dict, List, Union


class JSONReader:
    OBJECT_END = object()
    ARRAY_END = object()
    COLON = object()
    COMMA = object()
    FIRST, CURRENT, NEXT = range(3)

    escapes = {
        '"': '"',
        "\\": "\\",
        "/": "/",
        "b": "\b",
        "f": "\f",
        "n": "\n",
        "r": "\r",
        "t": "\t",
    }

    def __init__(self):
        self.it = None
        self.c = ""
        self.token = None
        self.buf = []

    def next(self) -> str:
        self.c = next(self.it, "")
        return self.c

    def skip_whitespace(self):
        while self.c and self.c.isspace():
            self.next()

    def read(self, string: str, start: int = NEXT) -> Any:
        self.it = iter(string)
        if start == self.FIRST:
            self.c = self.next()
        elif start == self.CURRENT:
            self.c = string[0]
        elif start == self.NEXT:
            self.c = self.next()
        return self._read()

    def _read(self) -> Any:
        self.skip_whitespace()
        ch = self.c
        self.next()
        if ch == '"':
            self.token = self._string()
        elif ch == "[":
            self.token = self._array()
        elif ch == "]":
            self.token = self.ARRAY_END
        elif ch == ",":
            self.token = self.COMMA
        elif ch == "{":
            self.token = self._object()
        elif ch == "}":
            self.token = self.OBJECT_END
        elif ch == ":":
            self.token = self.COLON
        elif ch == "t":
            self._consume_chars(3)  # consume 'rue'
            self.token = True
        elif ch == "f":
            self._consume_chars(4)  # consume 'alse'
            self.token = False
        elif ch == "n":
            self._consume_chars(3)  # consume 'ull'
            self.token = None
        else:
            self.it = iter([self.c] + list(self.it))  # rewind iterator
            if self.c.isdigit() or self.c == "-":
                self.token = self._number()
        return self.token

    def _consume_chars(self, num_chars: int):
        for _ in range(num_chars):
            self.next()

    def _object(self) -> Dict:
        result = {}
        key = self._read()
        while self.token != self.OBJECT_END:
            self._read()  # expect colon
            if self.token != self.OBJECT_END:
                result[key] = self._read()
                if self._read() == self.COMMA:
                    key = self._read()
        return result

    def _array(self) -> List:
        result = []
        value = self._read()
        while self.token != self.ARRAY_END:
            result.append(value)
            if self._read() == self.COMMA:
                value = self._read()
        return result

    def _number(self) -> Union[int, float, Decimal]:
        length = 0
        is_floating_point = False
        self.buf.clear()

        if self.c == "-":
            self._add()

        length += self._add_digits()
        if self.c == ".":
            self._add()
            length += self._add_digits()
            is_floating_point = True

        if self.c in "eE":
            self._add()
            if self.c in "+-":
                self._add()
            self._add_digits()
            is_floating_point = True

        num_str = "".join(self.buf)
        return (
            float(num_str)
            if is_floating_point
            else int(num_str) if length < 19 else Decimal(num_str)
        )

    def _add_digits(self) -> int:
        count = 0
        while self.c.isdigit():
            self._add()
            count += 1
        return count

    def _string(self) -> str:
        self.buf.clear()
        while self.c != '"':
            if self.c == "\\":
                self.next()
                if self.c == "u":
                    self._add(self._unicode())
                else:
                    self._add(self.escapes.get(self.c, self.c))
            else:
                self._add()
        self.next()  # consume closing quote
        return "".join(self.buf)

    def _unicode(self) -> str:
        hex_str = "".join(self.next() for _ in range(4))
        return chr(int(hex_str, 16))

    def _add(self, cc: str = None):
        if cc is None:
            cc = self.c
        self.buf.append(cc)
        self.next()
