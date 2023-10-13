import json

from pydantic import ValidationError
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.parser import parse
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler import Response, content_types

from my_cognito_lambda.exception.error_code_enum import ErrorCodeEnum
from my_cognito_lambda.exception.unauthorized_exception import UserPlatformDemoError
from my_cognito_lambda.models.user_create import UserCreate
from my_cognito_lambda.models.user_response import UserResponse
from my_cognito_lambda.services.user_service import UserService
from my_cognito_lambda.utils.authorized_validator import AuthorizedUserValidator
from my_cognito_lambda.utils.email_validator import EmailValidator

tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver()
auth_user = AuthorizedUserValidator()
email_validator = EmailValidator()
user_service = UserService()


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    logger.info("REQUEST CONTEXT: %s", context)

    return app.resolve(event, context)


@app.post("/users")
@tracer.capture_method
def create_user_event():
    context = app.current_event.request_context
    cognito_username = auth_user.is_authorize(context)
    logger.info("> get request contex: %s", context)

    payload_json = app.current_event['body']
    user_create = parse(event=payload_json, model=UserCreate)
    logger.info("> user create payload: %s", payload_json)

    email_validator.is_unique(user_create.email)

    user_service.create_user(user_create=user_create, cognito_username=cognito_username)

    return Response(status_code=201)


@app.get("/users")
@tracer.capture_method
def list_user_event():
    context = app.current_event.request_context
    cognito_username = auth_user.is_authorize(context)
    logger.info("> get request contex: %s", context)

    result = user_service.get_users(cognito_username)
    user_responses = [UserResponse(**item) for item in result]
    users = [user.to_dict() for user in user_responses]

    return Response(
        status_code=200,
        content_type=content_types.APPLICATION_JSON,
        body=json.dumps({"users": users}),
    )


@app.exception_handler(ValidationError)
def handle_validation_error(error: ValidationError) -> Response:
    return Response(
        status_code=400,
        content_type=content_types.APPLICATION_JSON,
        body=json.dumps({"detail": error.errors()}),
    )


@app.exception_handler(UserPlatformDemoError)
def handle_custom_errors(error: UserPlatformDemoError) -> Response:
    if error.code == ErrorCodeEnum.unauthorized:
        return Response(status_code=401)

    else:
        error_response = {"loc": error.location, "msg": error.message}

        return Response(
            status_code=400,
            content_type=content_types.APPLICATION_JSON,
            body=json.dumps({"detail": [error_response]}),
        )
