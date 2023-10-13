from enum import Enum


class ErrorCodeEnum(str, Enum):
    unauthorized = "Unauthorized"
    unique_email = "Email already exist"
    internal_error = "Internal error"
