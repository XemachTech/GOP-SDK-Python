class JSONValidator:

    def __init__(self, listener):
        self.listener = listener
        self.it = None
        self.c = None
        self.col = 0

    def validate(self, input: str) -> bool:
        input = input.strip()
        self.listener.start(input)
        ret = self.valid(input)
        self.listener.end()
        return ret

    def valid(self, input: str) -> bool:
        if input == "":
            return True

        ret = True
        self.it = iter(input)
        self.c = next(self.it, None)
        self.col = 1

        if not self.value():
            ret = self.error("value", 1)
        else:
            self.skip_white_space()
            if self.c is not None:
                ret = self.error("end", self.col)

        return ret

    def value(self) -> bool:
        return (
            self.literal("true")
            or self.literal("false")
            or self.literal("null")
            or self.string()
            or self.number()
            or self.object()
            or self.array()
        )

    def literal(self, text: str) -> bool:
        ci = iter(text)
        t = next(ci)
        if self.c != t:
            return False

        start = self.col
        ret = True
        for t in ci:
            if t != self.next_character():
                ret = False
                break
        self.next_character()

        if not ret:
            self.error(f"literal {text}", start)
        return ret

    def array(self) -> bool:
        return self.aggregate("[", "]", False)

    def object(self) -> bool:
        return self.aggregate("{", "}", True)

    def aggregate(
        self, entry_character: str, exit_character: str, prefix: bool
    ) -> bool:
        if self.c != entry_character:
            return False
        self.next_character()
        self.skip_white_space()

        if self.c == exit_character:
            self.next_character()
            return True

        while True:
            if prefix:
                start = self.col
                if not self.string():
                    return self.error("string", start)
                self.skip_white_space()
                if self.c != ":":
                    return self.error("colon", self.col)
                self.next_character()
                self.skip_white_space()

            if self.value():
                self.skip_white_space()
                if self.c == ",":
                    self.next_character()
                elif self.c == exit_character:
                    break
                else:
                    return self.error(f"comma or {exit_character}", self.col)
            else:
                return self.error("value", self.col)

            self.skip_white_space()

        self.next_character()
        return True

    def number(self) -> bool:
        if not self.c.isdigit() and self.c != "-":
            return False
        start = self.col

        if self.c == "-":
            self.next_character()

        if self.c == "0":
            self.next_character()
        elif self.c.isdigit():
            while self.c.isdigit():
                self.next_character()
        else:
            return self.error("number", start)

        if self.c == ".":
            self.next_character()
            if self.c.isdigit():
                while self.c.isdigit():
                    self.next_character()
            else:
                return self.error("number", start)

        if self.c in ["e", "E"]:
            self.next_character()
            if self.c in ["+", "-"]:
                self.next_character()
            if self.c.isdigit():
                while self.c.isdigit():
                    self.next_character()
            else:
                return self.error("number", start)

        return True

    def string(self) -> bool:
        if self.c != '"':
            return False

        start = self.col
        escaped = False

        self.next_character()
        while self.c is not None:
            if not escaped and self.c == "\\":
                escaped = True
            elif escaped:
                if not self.escape():
                    return False
                escaped = False
            elif self.c == '"':
                self.next_character()
                return True

            self.next_character()

        return self.error("quoted string", start)

    def escape(self) -> bool:
        start = self.col - 1
        if self.c not in '\\"/bfnrtu':
            return self.error(
                'escape sequence \\",\\\\,\\/,\\b,\\f,\\n,\\r,\\t or \\uxxxx', start
            )

        if self.c == "u":
            if (
                not self.ishex(self.next_character())
                or not self.ishex(self.next_character())
                or not self.ishex(self.next_character())
                or not self.ishex(self.next_character())
            ):
                return self.error("unicode escape sequence \\uxxxx", start)

        return True

    def ishex(self, d: str) -> bool:
        return d.lower() in "0123456789abcdef"

    def next_character(self) -> str:
        self.c = next(self.it, None)
        self.col += 1
        return self.c

    def skip_white_space(self):
        while self.c is not None and self.c.isspace():
            self.next_character()

    def error(self, type: str, col: int) -> bool:
        if self.listener:
            self.listener.error(type, col)
        return False
