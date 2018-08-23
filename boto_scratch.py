import boto3
import datetime
import dateutil
from secrets import *


session = boto3.Session(
    aws_access_key_id=key_id,
    aws_secret_access_key=key,
    region_name=region
)


def running(instance):
    return instance.state["Code"] == 16


def created_on(instance):
    return instance.launch_time


def time_difference(instance):
    td = created_on(instance)
    tm = datetime.datetime.now(tz=dateutil.tz.tz.tzutc()) - td
    hours, remainder = divmod(tm.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return datetime.time(minute=minutes, second=seconds)


def close_to_next_hour(time):
    return 60 - time.minute <= 2


ec2 = session.resource("ec2")
instance = list(ec2.instances.iterator())[0]
diff = close_to_next_hour(time_difference(instance))