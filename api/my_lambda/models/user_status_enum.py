from enum import Enum


class UserStatus(str, Enum):
    active = "ACTIVE"
    inactive = "INACTIVE"
    error = "ERROR"
