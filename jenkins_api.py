import os, json
import jenkinsapi
import requests
import boto3


NON_GPU_JOBS = ["goai-docker-container-builder", "gpu-instance-manager"]
JENKINS_URL = os.environ.get("JENKINS_URL", "")
AWS_CREDENTIALS_URL = os.environ.get("AWS_CREDENTIALS_URL", "")
AWS_KEY = ""
AWS_KEY_ID = ""


def get_jenkins_client(username, password):
    return jenkinsapi.Jenkins(JENKINS_URL, username, password)


def get_jobs():
    jenk = jenkinsapi.Jenkins(JENKINS_URL)
    jobs = []
    for item in jenk.items():
        if str(item[1]) in [str(job) for job in jobs]:
            continue
        elif str(item[1]) in NON_GPU_JOBS:
            continue
        jobs.append(item[1])
    return jobs


def jobs_running(jobs):
    running = [job.is_running() for job in jobs]
    return any(running)


if __name__ == "__main__":
    r = requests.get(AWS_CREDENTIALS_URL)
    creds = json.loads(r.text)
    print(creds)
    KEY_ID = creds["AccessKeyId"]
    KEY = creds["SecretAccessKey"]
    TOKEN = creds["Token"]
    ec2 = boto3.client(
        'ec2',
        aws_access_key_id=KEY_ID,
        aws_secret_access_key=KEY,
        aws_session_token=TOKEN,
        region_name="us-east-2"
    )
    iam = boto3.client(
        'iam',
        aws_access_key_id=KEY_ID,
        aws_secret_access_key=KEY,
        aws_session_token=TOKEN,
    )
    print(iam.get_policy(PolicyArn=os.environ.get("IAM_USER")))