import requests

from secrets import user, password

r = requests.get("http://18.191.94.64/job/goai-docker-container-builder/api/json?tree=builds", auth=(user, password))
print(r.text)