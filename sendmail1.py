from botocore.vendored import requests
import smtplib
import sys
import json
from email.mime.text import MIMEText 
import boto3
def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table= dynamodb.Table('Match_Fixture')
    with table.batch_writer() as batch:
      for i in range(24,29):
        batch.put_item(
        Item=   {
	    'match_id':i,
	    'team1':'MI',
	    'team2':'RCB',
	    'date': str(i)+'-02-2018',
	    'time': '16:30:00'
	}
 ) 


    
# creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
 
# start TLS for security
    s.ehlo()
    s.starttls()
    lst= ['yashnitrr@gmail.com','onkar.pathak@quantiphi.com','pradeep.tripathi@quantiphi.com','arvind.nair@quantiphi.com','yash.agrawal@quantiphi.com','rajat.dange@quantiphi.com','akshay.nar@quantiphi.com']
 
# Authentication
    s.login('yash.agrawal@gmail.com', '********')
    for i in range(0,len(lst)):
# message to be sent
        message = "Hi bidders, click on the below link to register yourself for bidding process. We will notify you before 6 hours when bidding will start. For Registration Click here:" +   "https://rajatdpe.auth.us-east-1.amazoncognito.com/login?response_type=code&client_id=34rs33humvs1mr6s7vmub02dof&redirect_uri=https://www.quantiphi.com"
        msg= MIMEText(u'<a href="https://rajatdpe.auth.us-east-1.amazoncognito.com/login?response_type=code&client_id=34rs33humvs1mr6s7vmub02dof&redirect_uri=https://dk183eivciki9.cloudfront.net/redirect.html">Click here for registration</a>','html')
        msg['Subject']= "Click on   link for registration"
        msg['From']= "IPL QuantBet"
# sending the mail
        s.sendmail('yash.agrawal@quantiphi.com',lst[i] ,msg.as_string())
# sending the mail
        #s.sendmail('yash.agrawal@gmail.com',lst[i] , message)
 
# terminating the session
    s.close()
    responseStatus = 'SUCCESS'
    responseData = {}
    if event['RequestType'] == 'Create':
        sendResponse(event, context, responseStatus, responseData)

    responseData = {'Success': 'Test Passed.'}
    sendResponse(event, context, responseStatus, responseData)
    return 'Hello from Lambda'


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
