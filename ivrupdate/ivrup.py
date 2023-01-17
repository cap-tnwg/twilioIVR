import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
import boto3
from os import getenv

logger = Logger()

# Establish DynamoDB client in handler so that it doesn't need to be created each runtime
ddb = boto3.client("dynamodb")
tablename = getenv("DYNAMO_TABLE")


def lambda_handler(event, context):
    # Extract the JSON from the body of the call
    body = json.dumps(event['body'])
    b2 = json.loads(json.loads(body))
    numbers = json.loads(b2['data'])
    for d in numbers:
        if d[0] == "Number":
            pass
        else:
            print(f"Title: {d[3]}: Number: {d[4]}")

    # Reformat the data to be used by downstream
    ddbdata = {
        "active": b2['active'],
        "message": b2['message'],
        "data": numbers
    }

    # Store it in DDB
    response = ddb.put_item(
        TableName=tablename,
        Item={
            "id": {"S": "1"},
            "data": {"S": json.dumps(ddbdata)},

        }
    )
    # Return SUCCESS!
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": json.dumps(ddbdata),
        }),
    }
