import os, json
import jenkinsapi
import requests
from jenkinsapi.jenkins import Jenkins


NON_GPU_JOBS = ["goai-docker-container-builder", "gpu-instance-manager"]
JENKINS_URL = os.environ.get("JENKINS_URL", "")
AWS_CREDENTIALS_URL = os.environ.get("AWS_CREDENTIALS_URL", "")


def get_jenkins_client(username, password):
    return Jenkins(JENKINS_URL, username, password)


def get_jobs():
    jenk = Jenkins(JENKINS_URL)
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
    print(jobs_running(get_jobs()))
    r = requests.get(AWS_CREDENTIALS_URL)
    print(json.loads(r.text).keys())
