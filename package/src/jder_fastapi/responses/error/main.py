from enum import Enum


class ResponseError(Enum):
    """
    Response error.
    """

    PARSE = "parse"
    """
    Validation error.
    """

    def to_code(self):
        """
        Get the error code.
        """
        return self.value

    def to_message(self):
        """
        Get the error message.
        """
        match self:
            case ResponseError.PARSE:
                return "Failed to parse the request"
