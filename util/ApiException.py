class ApiException(Exception):
    """
    International Open Platform common exception.

    Attributes:
        error_code (str): Error code for the exception.
        error_message (str): Error message for the exception.
    """

    def __init__(self, error_code=None, error_message=None, message=None, cause=None):
        """
        Initializes the ApiException instance.

        Args:
            error_code (str): Error code for the exception.
            error_message (str): Error message for the exception.
            message (str): Custom error message.
            cause (Exception): Original exception that caused this exception.
        """
        if error_code and error_message:
            super().__init__(f"{error_code}: {error_message}")
            self.error_code = error_code
            self.error_message = error_message
        elif message and cause:
            super().__init__(message, cause)
            self.error_code = None
            self.error_message = None
        elif message:
            super().__init__(message)
            self.error_code = None
            self.error_message = None
        elif cause:
            super().__init__(cause)
            self.error_code = None
            self.error_message = None
        else:
            super().__init__()
            self.error_code = None
            self.error_message = None

    def get_error_code(self):
        """
        Gets the error code of the exception.

        Returns:
            str: The error code.
        """
        return self.error_code

    def get_error_message(self):
        """
        Gets the error message of the exception.

        Returns:
            str: The error message.
        """
        return self.error_message
