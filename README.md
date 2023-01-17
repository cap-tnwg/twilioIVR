# twilioIVR

This project contains source code and supporting files for a serverless AWS application that receives data from a Google Sheets document for configuration, and uses that information to manage an Interactive Voice Response (IVR) system to assist CAP TNWG with mission base communications.

It consists of 3 AWS Lambda functions (Python 3.9 Runtime), an AWS API Gateway, and a DynamoDB table to store and retrieve configuration.

## ivrupdate
This function is tied to the /ivrUpdate path on the API Gateway.  It receives a "POST" call from the Google Sheets app that delivers data in a JSON format. That JSON is then stored in DynamoDB for use of the other functions. It returns a 200 upon completion.

## ivrCall
This function is the endpoint called by Twilio upon receiving a call.  It will check if the IVR is active. If not, it will forward the call to TNWG HQ automatically.

If the IVR is Active, it will play the requested message and wait for the user to enter a digit on the phone.  

This function returns a "twiml" XML formatted response. It specifies the endpoint of the ivrForward function for callbacks by Twilio. As such, the ivrForward function will be called by Twilio when a digit is entered.

## ivrForward
This function receives a POST call from Twilio when entered. It will then extract the "Digits" parameter from the call, and check if there is a forwarding number associated with that digit.  If not, it will play a message about an invalid response, and ask the user to select again. If a valid digit is entered, TWIML XML is returned to forward the call to the specified number.
