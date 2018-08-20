import boto3
from secrets import *


ec2 = boto3.client(
    'ec2',
    aws_access_key_id=key_id,
    aws_secret_access_key=key,
    region_name=region
)