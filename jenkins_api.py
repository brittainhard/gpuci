import datetime

import jenkinsapi
from jenkinsapi.jenkins import Jenkins

j = Jenkins("http://18.191.94.64/")
jobs = []
for item in j.items():
    jobs.append(item[1])

last = [job.get_last_good_build().get_timestamp() for job in jobs]
now = datetime.datetime.now(tz=datetime.timezone.utc)
now = now.replace(second=0, microsecond=0)
print(now)