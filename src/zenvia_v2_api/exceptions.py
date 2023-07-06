"""Create custom exceptions for Zenvia Python API."""


class ZenviaAPIException(Exception):
    pass


class ZenviaAPIRequestException(ZenviaAPIException):
    pass


class ZenviaAPIFunctionValidation(ZenviaAPIException):
    pass
