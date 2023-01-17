# This function is called by Twilio upon the receipt of a call.
# It checks for the IVR being active and presents the menu for the caller.

import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
import boto3
from os import getenv

logger = Logger()
# Setting up DynamoDB client outside the handler
ddb = boto3.client('dynamodb')
tablename = getenv("DYNAMO_TABLE")
url = getenv("URL")


def lambda_handler(event, context):

    # Grab data from DynamoDB
    data = ddb.get_item(
        TableName=tablename,
        # Only one row in table, so ID is always 1
        Key={
            'id': {'S': '1'},
        }
    )

    # parse the data to a dictionary
    data = json.loads(data['Item']['data']['S'])

    # Check if the "active" flag is set
    if not data['active']:
        # If not, forward call to Wing HQ directly
        twimlresponse = """<?xml version="1.0" encoding="UTF-8"?> 
                                <Response> 
                                    <Dial>8653424880</Dial> 
                                </Response>"""
    else:
        # if not, present the menu as configured. Point twilio to the ivrForward function (url) upon caller selecting an option
        twimlresponse = f"""<?xml version="1.0" encoding="UTF-8"?>
                                <Response>
                                    <Gather timeout="10" numDigits="1" method="POST" action = "{url}" >
                                        <Say>{data['message']}</Say>
                                    </Gather>
                                </Response>"""
    # return TWIML to Twilio
    return {
        "statusCode": 200,
        "body": twimlresponse,
        # Make sure you set Content-Type to application/xml or text/xml as expected by Twilio.
        "headers": {
            "Content-Type": """text/xml"""
        }

        # "location": ip.text.replace("\n", "")
    }
