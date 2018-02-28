import boto3
from botocore.vendored import requests
from boto3.dynamodb.conditions import Key, Attr
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Bidder')
    response = table.scan(FilterExpression=Attr('total_amount').gt(0))
    #for i in response:
    items = response['Items']
    
    list1=[]
    #list2=[]
    for i in items:
        for key,item in i.items():
            a=i['email']
            #b=i['amount']
        list1.append(a)
        #list2.append(b)
            
    print(list1)
    
   
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.ehlo()
    s.starttls()
#   lst = ['rajat.dange@quantiphi.com', 'akshay.nar@quantiphi.com', 'arvind.nair@quantiphi.com',
 #         'pranita.kadge@quantiphi.com', 'yashnitrr@gmail.com']
    s.login('yash.agrawal@gmail.com', '******')
    
    msg= MIMEText(u'<a href="http://34.230.61.139:10080/">Click here for Bidding</a>','html')
    msg['Subject']= "Click on link for bidding"
    msg['From']= "IPL QuantBet"
# sending the mail
    for j in range (0,len(list1)):   
        s.sendmail('yash.agrawal@gmail.com', list1[j] ,msg.as_string())

    # Authentication
    
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


