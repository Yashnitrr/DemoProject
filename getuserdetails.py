import boto3
import re
import json
import smtplib
from email.mime.text import MIMEText
from botocore.vendored import requests

users = []
non_quantiphi_users = []

client = boto3.client('cognito-idp')
db = boto3.client('dynamodb')


def lambda_handler(event, context):
    response = client.list_users(
        UserPoolId='us-east-1_2aoKvlGeg',
        AttributesToGet=[
            'email',
        ],

    )
    d1 = response['Users']
    for i in range(len(d1)):

        temp = d1[i]['Attributes'][0]['Value']
        if (re.match('[a-z]+\.[a-z]+@quantiphi\.com$', temp)):
            db.put_item(TableName='Bidder', Item={'email': {'S': temp}, 'total_amount': {'N': '50'}, 'bid': {'N': '0'}})
            users.append(temp)
        else:
            non_quantiphi_users.append(temp)

    s = smtplib.SMTP('smtp.gmail.com', 587)

            # start TLS for security
    s.ehlo()
    s.starttls()
    #lst = ['yashnitrr@gmail.com']

            # Authentication
    s.login('yash.agrawal@gmail.com', '****')
    for i in range(0, len(non_quantiphi_users)):
            # message to be sent
        message = "You have not been registered , only Quantiphi users are allowed."

            # sending the mail
        s.sendmail('yash.agrawal@quantiphi.com', non_quantiphi_users[i], message)
            # sending the mail
            # s.sendmail('yash.agrawal@quantiphi.com',lst[i] , message)

            # terminating the session
    for i in range(0, len(users)):
        # message to be sent
        conf_message = "Thank you for your registration. You will receive an email before the bidding starts"
        # sending the mail
        s.sendmail('yash.agrawal@gmail.com', users[i], conf_message)
    s.close()
    responseStatus = 'SUCCESS'
    responseData = {}
    if event['RequestType'] == 'Create':
        sendResponse(event, context, responseStatus, responseData)

    responseData = {'Success': 'Test Passed.'}
    sendResponse(event, context, responseStatus, responseData)
    return

def sendResponse(event, context, responseStatus, responseData):
	responseBody = {'Status': responseStatus,
	'Reason': 'See the details in CloudWatch Log Stream: ' + context.log_stream_name,
	'PhysicalResourceId': context.log_stream_name,
	'StackId': event['StackId'],
	'RequestId': event['RequestId'],
	'LogicalResourceId': event['LogicalResourceId'],
	'Data': responseData}
	print ('RESPONSE BODY:n' + json.dumps(responseBody))
	try:
		req = requests.put(event['ResponseURL'], data=json.dumps(responseBody))
		if req.status_code != 200:
			print (req.text)
			raise Exception('Recieved non 200 response while sending response to CFN.')
		return
	except requests.exceptions.RequestException as e:
		print (e)
		raise