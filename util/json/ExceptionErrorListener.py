from util.json.BufferErrorListener import BufferErrorListener


class ExceptionErrorListener(BufferErrorListener):
    def error(self, error_type: str, col: int):
        """
        Handles an error by logging the error type and column,
        then raises an IllegalArgumentException.

        :param error_type: Type of error
        :param col: Column where the error occurred
        :raises ValueError: with the current buffer content
        """
        super().error(error_type, col)
        raise ValueError(self.buffer)
