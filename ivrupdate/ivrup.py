import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
import boto3
from os import getenv

logger = Logger()

ddb = boto3.client("dynamodb")
tablename = getenv("DYNAMO_TABLE")


def lambda_handler(event, context):
    body = json.dumps(event['body'])
    print(body)
    # print(f"Body: {body}")

    b2 = json.loads(json.loads(body))
    print(f"B2: {b2}")
    # active=b2['active']
    print(f"Active: b2['active']\nMessage: {b2['message']}\n")
    numbers = json.loads(b2['data'])
    for d in numbers:
        if d[0] == "Number":
            pass
        else:
            print(f"Title: {d[3]}: Number: {d[4]}")

    ddbdata = {
        "active": b2['active'],
        "message": b2['message'],
        "data": numbers
    }

    response = ddb.put_item(
        TableName=tablename,
        Item={
            "id": {"S": "1"},
            "data": {"S": json.dumps(ddbdata)},

        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
