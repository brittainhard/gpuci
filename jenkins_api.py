import requests

from secrets import user, password

# r = requests.get("http://18.191.94.64/job/goai-docker-container-builder/api/json?tree=builds", auth=(user, password))

import jenkinsapi
from jenkinsapi.jenkins import Jenkins

j = Jenkins("http://18.191.94.64/")
jobs = []
for item in j.items():
    jobs.append(item[1])

last_good_jobs = [job.get_last_good_build().get_timestamp() for job in jobs]