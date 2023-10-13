from aws_lambda_powertools.utilities.data_classes.api_gateway_proxy_event import APIGatewayEventRequestContext
from aws_lambda_powertools import Logger, Tracer

logger = Logger()


class ContextExtractor:

    @classmethod
    def extract(cls: "ContextExtractor", context: APIGatewayEventRequestContext) -> str | None:
        try:
            authorizer_claims = context.authorizer.get("claims", {})
            cognito_username = authorizer_claims.get("cognito:username", None)
            logger.info("cognito username: %s", cognito_username)
            return cognito_username

        except (KeyError, AttributeError):
            logger.warning("cognito:username not defined.")
            return None
