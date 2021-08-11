import boto3

from DataProvider.database_handler.constants import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION


def get_client():
    my_session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                                       aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                       region_name=REGION)

    db_client = my_session.client("dynamodb")
    return db_client
