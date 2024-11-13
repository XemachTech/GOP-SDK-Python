from abc import ABC, abstractmethod


class JSONErrorListener(ABC):
    @abstractmethod
    def start(self, text: str):
        """
        Called when starting to process a new JSON input.

        :param text: The input text to process.
        """
        pass

    @abstractmethod
    def error(self, message: str, column: int):
        """
        Called when an error occurs.

        :param message: Error message describing the issue.
        :param column: The column number where the error occurred.
        """
        pass

    @abstractmethod
    def end(self):
        """
        Called when processing the JSON input ends.
        """
        pass
