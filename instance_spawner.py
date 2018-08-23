import boto3
import jenkinsapi


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
    ec2 = session.resource('ec2')
    instances = list(ec2.instances.terator())