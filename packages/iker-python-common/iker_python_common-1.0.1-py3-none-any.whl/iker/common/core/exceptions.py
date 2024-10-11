import traceback


class BaseTraceableException(Exception):
    """
    Base class of traceable exceptions and errors
    """

    def __init__(self, message: str, *args, **kwargs):
        super(BaseTraceableException, self).__init__()
        self.message = message
        self.args = args
        self.cause = kwargs.get("cause")
        self.traceback = "" if kwargs.get("cause") is None else traceback.format_exc()

    def __str__(self) -> str:
        return self.message % self.args

    def __traceback(self):
        if self.cause is None or not isinstance(self.cause, BaseTraceableException):
            return self.traceback
        return self.traceback + self.cause.__traceback()

    @staticmethod
    def format_traceback(error):
        if isinstance(error, BaseTraceableException):
            return traceback.format_exc() + error.__traceback()
        return traceback.format_exc()


class RuntimeException(BaseTraceableException):
    """
    Represents runtime exception
    """

    def __init__(self, message: str, *args, **kwargs):
        super(RuntimeException, self).__init__(message, *args, **kwargs)


class InvalidTypeException(BaseTraceableException):
    """
    Represents invalid type exception
    """

    def __init__(self, message: str, *args, **kwargs):
        super(InvalidTypeException, self).__init__(message, *args, **kwargs)


class InvalidKeyException(BaseTraceableException):
    """
    Represents invalid key exception
    """

    def __init__(self, message: str, *args, **kwargs):
        super(InvalidKeyException, self).__init__(message, *args, **kwargs)


class InvalidValueException(BaseTraceableException):
    """
    Represents invalid value exception
    """

    def __init__(self, message: str, *args, **kwargs):
        super(InvalidValueException, self).__init__(message, *args, **kwargs)
