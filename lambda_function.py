from __future__ import absolute_import, unicode_literals
import json
import urllib.parse
import boto3
import re

PATTERN = r'^(\d{8}T\d{2}:\d{2}) - (\w+) - (\w+)( \[\d\])?: (.+)$'
PATTERN_SEVERITY = r'^(\d{8}T\d{2}:\d{2}) - (\w+) - (\w+) \[(\d)\]: (.+)$'
PATTERN_STAKEHOLDERS = r'^(.+) - (\w+) - (\w+)$'

s3 = boto3.client('s3')
sns = boto3.client('sns')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    eventname = event['Records'][0]['eventName']
    sns_message = str("This Email Represent a File Status has been Changed in One of Your Bucket \n\n BUCKET NAME: "+ bucket +"\n\n FILE NAME: " + key + "\n\n OPERATION: " + eventname + "\n\n")
    try:
        if not eventname.startswith("ObjectCreated"):
            return
        response = s3.get_object(Bucket='bucket2', Key='stakeholders.txt')
        content = response['Body'].read().decode('utf-8')
        names = get_stakeholders(content)
        
        response = s3.get_object(Bucket=bucket, Key=key)
        subject= "Latest Application Logs"
        for x in names:
            query = {'CATEGORY':x['category'], 'APPLICATION': x['application']}
            log = filtering_log(response['Body'], query )
            sns_message = '\n'.join(log)
               
            # # sns_response = sns.publish(
            # #     TargetArn='arn:aws:sns:us-east-1:12345678:bucket1',
            # #     Message= str(sns_message),
            # #     Subject= str(subject)
            # )
            notify(x['email'], sns_message)
            
        return response['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

def convert_to_string(data):
    content = data.read().decode("utf-8")
    return content
    
def get_stakeholders(content):
    result = []
    lines = content.split('\n')
    for line in lines:
        if not line:
            continue
        found = re.search(PATTERN_STAKEHOLDERS, line)
        if not found:
            continue
        email = found.group(1)
        application = found.group(2)
        category = found.group(3)
        
        result.append({'email': email, 'application': application, 'category': category})
        
    return result 
    
def filtering_log(data, query):
    content = convert_to_string(data)
    result = []
    lines = content.split('\n')
    for line in lines:
        if not line:
            continue
        found = re.search(PATTERN, line)
        if not found:
            continue
        if 'TIMESTAMP' in query and found.group(1) != query['TIMESTAMP']:
            continue
        if 'APPLICATION' in query and found.group(2) != query['APPLICATION']:
            continue
        if 'CATEGORY' in query and found.group(3) != query['CATEGORY']:
            continue

        if 'SEVERITY' in query:
            found = re.search(PATTERN_SEVERITY, line)
            if not found:
                continue
            if int(found.group(4)) != query['SEVERITY']:
                continue
       
        result.append(line)
    return result

    
   