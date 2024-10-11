class SladeException(Exception):
    def __init__(self, message):
        super().__init__(message)


class QueryFailedException(SladeException):
    def __init__(self, message):
        super().__init__(message)
