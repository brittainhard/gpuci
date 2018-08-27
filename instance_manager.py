import os, json, argparse
import datetime, dateutil

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


def get_instances():
    return list(rs.instances.iterator())


def instance_is_running(instance):
    return instance.state["Code"] == 16


def get_running_instances(instances):
    running_instances = []
    for x in instances:
        if instance_is_running(x):
            running_instances.append(x)
    return running_instances


def get_gpu_instance(instances):
    for x in instances:
        print(x.image.id)
        if x.image.id == AMI:
            return x
    return None


def attach_elastic_ip(instance):
	try:
		response = cl.associate_address(AllocationId=EIP,
										 InstanceId=instance.id)
		print(response)
	except ClientError as e:
		print(e)


def create_gpu_instance():
    instances = rs.create_instances(
        ImageId=AMI,
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=[SECURITY_GROUP],
        InstanceType=INSTANCE_SIZE,
    )

    status = None
    while not status:
        status = cl.describe_instance_status(Filters=
            [
                {
                    "Name": "instance-state-name",
                    "Values": ["running"]
                }
            ],InstanceIds=[instances[0].id]
        )["InstanceStatuses"]
        print("Not Running.")
        time.sleep(5)
    return instances[0]


def spawn_instances(dry_run=False):
    instances = get_instances()
    running = get_running_instances(instances)
    gpu = get_gpu_instance(running)
    if gpu:
        return
    elif dry_run:
        return
    else:
        instance = create_gpu_instance()
        attach_elastic_ip(instances[0])


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


def time_difference(instance):
    tm = datetime.datetime.now(tz=dateutil.tz.tz.tzutc()) - instance.launch_time
    hours, remainder = divmod(tm.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return datetime.time(minute=minutes, second=seconds)


def close_to_next_hour(instance):
    return 60 - time_difference(instance).minute <= 2


def terminate_instance(instance):
    instance.terminate()


def manage_instances(dry_run=False):
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
    rs = session.resource('ec2')
    cl = session.client('ec2')

    parser = argparse.ArgumentParser("Spawns instances and checks for instance statuses.")
    parser.add_argument("--spawn-instances", dest="instance_spawner",
        action="store_true", default=False)
    parser.add_argument("--manage-instances", dest="instance_manager",
        action="store_true", default=False)
    parser.add_argument("--dry-run", dest="dry_run",
        action="store_true", default=False)
    args = parser.parse_args()
    if args.instance_spawner and args.instance_manager:
        exit("Cannot spawn and manage instances at the same time.")
    elif not args.instance_spawner and not args.instance_manager:
        exit("Please specify either --spawn-instances or --manage-instances.")
    elif args.instance_spawner:
        spawn_instances(args.dry_run)
    elif args.instance_manager:
        manage_instances(dry_run)
