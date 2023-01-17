# This function is called by Twilio with digits when entered during a call.
# It keys on the Digits= parameter that is passed.

import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
import boto3
from os import getenv

logger = Logger()
# Establish DDB connection outside handler and load environment variables
ddb = boto3.client('dynamodb')
tablename = getenv("DYNAMO_TABLE")
url = getenv("URL")
# table = ddb_res.Table(tablename)


def lambda_handler(event, context):
    # Get the body of the call.  There are a number of parameters separated by &'s, so split it into a list
    body = event['body'].split("&")
    # Loop the list to find the Digits parameter
    for b in body:
        if b.startswith("Digits="):
            # Grab only the digit, convert to INT
            digit = int(b[-1:])
    # Grab the configuration from DDB
    # I considered grabbing this from outside the handler, but the config is meant to be dynamic, and don't want it only being grabbed once and becoming stale
    # ** Future enhancement ** Might want to make the ivrupdate function trigger something to make this function cold-start on a change so we can reduce DDB reads
    data = ddb.get_item(
        TableName=tablename,
        Key={
            # Table only has one row, ID == 1
            'id': {'S': '1'},
        }
    )
    # extract the digit from the JSON
    data = json.loads(data['Item']['data']['S'])
    num = data['data'][digit]

    # Col 1 in the GSheets file contains a "True/False" if there is a valid number available to diail, so check it
    if not num[1]:
        # If it's false, tell caller it's no good and repeat the menu
        twimlresponse = f"""<?xml version="1.0" encoding="UTF-8"?>
                                <Response>
                                    <Gather timeout="10" numDigits="1" method="POST" action = "{url}" >
                                        <Say>That option is not valid,,{data['message']}</Say>
                                    </Gather>
                                </Response>"""
    else:
        # If there is a number, grab it and forward the user there.
        fwdNum = num[4]
        twimlresponse = f"""<?xml version="1.0" encoding="UTF-8"?> 
                                <Response> 
                                    <Dial>{fwdNum}</Dial> 
                                </Response>"""
    # Return the TWIML response
    return {
        "statusCode": 200,
        "body": twimlresponse,
        # Make sure you set the Content-Type header to application/xml or text/xml that Twilio expects
        "headers": {
            "Content-Type": """text/xml"""
        }
    }
