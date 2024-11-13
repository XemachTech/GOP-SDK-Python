from util.json.JSONReader import JSONReader
from util.json.JSONValidator import JSONValidator
from util.json.ExceptionErrorListener import ExceptionErrorListener


class JSONValidatingReader(JSONReader):
    INVALID = object()  # This is the equivalent of a constant INVALID in Python

    def __init__(self, validator=None):
        if validator is None:
            validator = JSONValidator(ExceptionErrorListener())  # Default behavior
        self.validator = validator
        super().__init__()

    def read(self, string: str) -> object:
        # if not self.validator.valid(string):
        #     return self.INVALID
        return super().read(string)
