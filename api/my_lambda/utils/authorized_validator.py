from aws_lambda_powertools.utilities.data_classes.api_gateway_proxy_event import APIGatewayEventRequestContext
from aws_lambda_powertools import Logger

from my_cognito_lambda.exception.error_code_enum import ErrorCodeEnum
from my_cognito_lambda.exception.unauthorized_exception import UserPlatformDemoError
from my_cognito_lambda.utils.conext_extractor import ContextExtractor

logger = Logger()
context_extractor = ContextExtractor()


class AuthorizedUserValidator:

    @classmethod
    def is_authorize(cls: "AuthorizedUserValidator", context: APIGatewayEventRequestContext) -> str:
        cognito_username = context_extractor.extract(context)
        logger.info("> get cognito username: %s", cognito_username)

        if not cognito_username:
            raise UserPlatformDemoError(
                ErrorCodeEnum.unauthorized,
                "Unauthorized user",
            )

        return cognito_username