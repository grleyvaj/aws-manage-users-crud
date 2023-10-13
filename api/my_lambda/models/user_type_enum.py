from enum import Enum


class UserType(str, Enum):
    admin = "ADMIN"
    invite = "INVITED"
