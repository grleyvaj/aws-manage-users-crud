from typing import Any

from my_cognito_lambda.exception.error_code_enum import ErrorCodeEnum


class UserPlatformDemoError(Exception):

    def __init__(
            self: "UserPlatformDemoError",
            code: ErrorCodeEnum,
            message: str,
            location: list[Any]
    ) -> None:
        self.code = code
        self.message = message
        self.location = location
        super().__init__(self.message)
