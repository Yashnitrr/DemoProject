import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.vendored import requests
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Bidder')
    response = table.scan(FilterExpression=Attr('total_amount').gt(-1))
    # for i in response:
    items = response['Items']

    list1 = []
    list2 = []
    for i in items:
        for key, item in i.items():
            a = i['email']
            b = i['total_amount']
        list1.append(a)
        list2.append(b)

    print(list1, list2)

    for k in range(0, len(list2)):
        for j in range(0, len(list1) - 1):
            if (list2[j] > list2[j + 1]):
                temp = list2[j]
                list2[j] = list2[j + 1]
                list2[j + 1] = temp
                temp1 = list1[j]
                list1[j] = list1[j + 1]
                list1[j + 1] = temp1
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.ehlo()
    s.starttls()
    #   lst = ['rajat.dange@quantiphi.com', 'akshay.nar@quantiphi.com', 'arvind.nair@quantiphi.com',
    #         'pranita.kadge@quantiphi.com', 'yashnitrr@gmail.com']

    # Authentication
    s.login('yash.agrawal@gmail.com', '*********')
    st = ""
    em = ""
    em += "MI has won the match!!!" + "\n\n"
    em += "Email                                             " + "Amount" + "\n"
    for i in range(0, len(list1)):
        em += "-----------------------------------------------------------" + "\n"
        em += list1[len(list1) - i - 1] + "                    " + str(list2[len(list1) - i - 1]) + "\n"
        # em+="----------------------------------------------------"+"\n"

    for j in range(0, len(list1)):
        print (list1[j])
        print (list2[j])

        s.sendmail('yash.agrawal@gmail.com', list1[j], em)

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



