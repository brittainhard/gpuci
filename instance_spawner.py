import boto3
from botocore.exceptions import ClientError
import datetime
import dateutil


SECURITY_GROUP = os.environ.get("SECURITY_GROUP", "")
AMI = os.environ.get("AMI", "")
ELASTIC_IP = os.environ.get("ELASTIC_IP", "")


def attach_elastic_ip(instance):
	try:
		response = cl.associate_address(AllocationId=EIP,
										 InstanceId=instance.id)
		print(response)
	except ClientError as e:
		print(e)


def create_instance():
    instances = ec2.create_instances(
        ImageId=AMI,
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=[SECURITY_GROUP],
        InstanceType=INSTANCE_SIZE,
    )
    return instances


if __name__ == "__main__":
    r = requests.get(AWS_CREDENTIALS_URL)
    creds = json.loads(r.text)
    AWS_KEY_ID = creds["AccessKeyId"]
    AWS_KEY = creds["SecretAccessKey"]
    AWS_SESSION_TOKEN = creds["Token"]
    session = boto3.Session(
        aws_access_key_id=AWS_KEY_ID,
        aws_secret_access_key=AWS_KEY,
        aws_session_token=AWS_SESSION_TOKEN,
        region_name="us-east-2"
    )
    ec2 = session.client('ec2')
