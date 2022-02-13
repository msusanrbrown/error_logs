import re

from logger.converter import convert_to_string
from logger.patterns import PATTERN




def process_log(data):
    
    content = convert_to_string(data)
    result = {'ErrorCount':0, 'SuccessCount':0, 'Total':0}
    lines = content.split('\n')
    for line in lines:
        if not line:
            continue
        found = re.search(PATTERN, line)
        if not found:
            continue
        category = found.group(3)
        if category == 'ERROR':
            result['ErrorCount']+=1
        elif category == 'SUCCESS':
            result['SuccessCount']+=1
        result['Total']+=1

    return result









def get_log_stats(bucket, key):
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key=key)
    emailcontent = response['Body'].read().decode('utf-8')


