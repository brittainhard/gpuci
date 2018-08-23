import os, json
import datetime
import dateutil

import jenkinsapi
import requests
import boto3


NON_GPU_JOBS = ["goai-docker-container-builder", "gpu-instance-manager"]
JENKINS_URL = os.environ.get("JENKINS_URL", "")
AWS_CREDENTIALS_URL = os.environ.get("AWS_CREDENTIALS_URL", "")
AWS_KEY = ""
AWS_KEY_ID = ""

SECURITY_GROUP = os.environ.get("SECURITY_GROUP", "")
AMI = os.environ.get("AMI", "")
ELASTIC_IP = os.environ.get("ELASTIC_IP", "")


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


def running(instance):
    return instance.state["Code"] == 16


def time_difference(instance):
    tm = datetime.datetime.now(tz=dateutil.tz.tz.tzutc()) - instance.launch_time
    print(tm)
    hours, remainder = divmod(tm.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return datetime.time(minute=minutes, second=seconds)


def close_to_next_hour(instance):
    return 60 - time_difference(instance).minute <= 2


def get_gpu_instance(instances):
    for x in instances:
        print(x.image.id)
        if x.image.id == AMI:
            return x
    return None


def manage_instance(instance):
    pass


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
    cl = session.clientj('ec2')
    instances = list(ec2.instances.iterator())
    print(close_to_next_hour(instances[0]))
    print(get_gpu_instance(instances))
    cl.describe_instances()