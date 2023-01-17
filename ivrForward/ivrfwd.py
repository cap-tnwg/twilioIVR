import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
import boto3
from os import getenv

logger = Logger()
ddb = boto3.client('dynamodb')
tablename = getenv("DYNAMO_TABLE")
url = getenv("URL")
# table = ddb_res.Table(tablename)


def lambda_handler(event, context):

    logger.info(event)

    body = event['body'].split("&")
    print(body)
    for b in body:
        print(b)
        if b.startswith("Digits="):
            digit = int(b[-1:])
    print(f"Digit: {digit}")
    data = ddb.get_item(
        TableName=tablename,
        Key={
            'id': {'S': '1'},
        }
    )
    # print(data.typeof())
    print(data['Item']['data']['S'])
    data = json.loads(data['Item']['data']['S'])
    num = data['data'][digit]

    if not num[1]:
        twimlresponse = f"""<?xml version="1.0" encoding="UTF-8"?>
                                <Response>
                                    <Gather timeout="10" numDigits="1" method="POST" action = "{url}" >
                                        <Say>That option is not valid,,{data['message']}</Say>
                                    </Gather>
                                </Response>"""
    else:
        fwdNum = num[4]
        twimlresponse = f"""<?xml version="1.0" encoding="UTF-8"?> 
                                <Response> 
                                    <Dial>{fwdNum}</Dial> 
                                </Response>"""
        # twimlresponse = f"""<?xml version="1.0" encoding="UTF-8"?>
        #                         <Response>
        #                                 <Say>Forwarding to {fwdNum}</Say>
        #                         </Response>"""

    return {
        "statusCode": 200,
        "body": twimlresponse,
        "headers": {
            "Content-Type": """text/xml"""
        }

        # "location": ip.text.replace("\n", "")
    }
