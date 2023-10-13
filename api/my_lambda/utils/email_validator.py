import boto3

from aws_lambda_powertools import Logger

from my_cognito_lambda.exception.error_code_enum import ErrorCodeEnum
from my_cognito_lambda.exception.unauthorized_exception import UserPlatformDemoError

dynamodb_table_name = 'users'
dynamodb_client = boto3.resource('dynamodb')
table = dynamodb_client.Table(dynamodb_table_name)

logger = Logger()


class EmailValidator:

    @classmethod
    def is_unique(cls: "EmailValidator", email: str):
        response = table.query(
            IndexName='email-index',
            KeyConditionExpression='email = :email',
            ExpressionAttributeValues={':email': email}
        )
        logger.info("> response when validate unique email: %s", response)

        if response.get('Count', 0) > 0:
            raise UserPlatformDemoError(
                ErrorCodeEnum.unique_email,
                f'Email already exist: {str(email)}',
                ["email"]
            )
