import io
from util.json.JSONErrorListener import (
    JSONErrorListener,
)


class BufferErrorListener(JSONErrorListener):
    def __init__(self, buffer=None):
        """
        Initializes the BufferErrorListener with an optional buffer.

        :param buffer: Optional, a pre-existing buffer (io.StringIO); if None, creates a new buffer.
        """
        self.buffer = buffer if buffer is not None else io.StringIO()
        self.input = ""

    def start(self, input_text: str):
        """
        Resets the listener with new input and clears the buffer.

        :param input_text: Input string to process.
        """
        self.input = input_text
        self.buffer = io.StringIO()  # Clear buffer by resetting it

    def error(self, error_type: str, col: int):
        """
        Records an error message in the buffer based on the type and column of the error.

        :param error_type: Expected type description of the error.
        :param col: Column where the error occurred.
        """
        self.buffer.write(f"expected {error_type} at column {col}\n")
        self.buffer.write(f"{self.input}\n")
        self.buffer.write(self._indent(col - 1) + "^\n")

    def _indent(self, n: int) -> str:
        """
        Generates a string with spaces for indentation.

        :param n: Number of spaces to indent.
        :return: A string containing `n` spaces.
        """
        return " " * n

    def end(self):
        """
        Placeholder for end of processing. Can be extended if needed.
        """
        pass
