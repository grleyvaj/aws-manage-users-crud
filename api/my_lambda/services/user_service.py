import boto3
import uuid

from datetime import datetime
from aws_lambda_powertools.event_handler import Response
from boto3.dynamodb.conditions import Attr

from my_cognito_lambda.exception.error_code_enum import ErrorCodeEnum
from my_cognito_lambda.exception.unauthorized_exception import UserPlatformDemoError
from my_cognito_lambda.models.user_type_enum import UserType
from my_cognito_lambda.models.user_create import UserCreate
from my_cognito_lambda.models.user_status_enum import UserStatus
from my_cognito_lambda.utils.token_generator import TokenGenerator

token_generator = TokenGenerator()

dynamodb_client = boto3.resource('dynamodb')
dynamodb_table_name = 'users'
table = dynamodb_client.Table(dynamodb_table_name)


class UserService:

    @classmethod
    def create_user(cls: "UserService", user_create: UserCreate, cognito_username: str):
        try:
            table.put_item(
                Item={
                    'user_id': str(uuid.uuid4()),
                    'email': user_create.email,
                    'name': user_create.name,
                    'last_name': user_create.last_name,
                    'charge': user_create.charge,
                    'type': UserStatus.inactive.value,
                    'status': UserType.invite.value,
                    'tenant_id': cognito_username,
                    'token_invite': token_generator.generate(user_create.email),
                    'created_at': (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
                }
            )
            return Response(status_code=201)

        except Exception as e:
            raise UserPlatformDemoError(
                ErrorCodeEnum.internal_error,
                f'Error creating user: {str(e)}',
            )

    @classmethod
    def get_users(cls: "UserService", cognito_username: str):
        try:
            response = table.scan(
                FilterExpression=Attr('tenant_id').eq(cognito_username)
            )

            return response['Items']

        except Exception as e:
            raise UserPlatformDemoError(
                ErrorCodeEnum.internal_error,
                f'Error listing users: {str(e)}',
            )
