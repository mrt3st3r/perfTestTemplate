from locust import HttpLocust, TaskSet, task
import json
import configparser
from logbook import Logger, StreamHandler, log
import sys

# loading the config file
config = configparser.ConfigParser()
config.read('conf.cnf')

# loading the values fomr teh config file
apikey = config.get('API', 'MYAPIKEY')
validStatusCode = config.get('STATUSCODES', 'VALID')
baseurl = config.get('API', 'BASEURL')
endpoint_X = config.get('API', 'ENDPOINT_X')

payload = config.get('PAYLOAD', 'payload')

minWait = config.get('WAIT_TIME', 'minWait')
maxWait = config.get('WAIT_TIME', 'maxWait')


# setting up the logger
StreamHandler(sys.stdout).push_application()
log = Logger('Logbook')

# setting up the proxies
port = config.get('PORT', 'PORT')
httpproxy = config.get('PROXIES', 'HTTP')
httpsproxy = config.get('PROXIES', 'HTTPS')
proxies = {'http': httpproxy + ":" + port, 'https': httpsproxy + ":" + port}



class APICalls(TaskSet):

    @task()
    def first_task(self):
        r = self.client.post(endpoint_X, data=json.dumps(payload), headers={'APIKEY': apikey})
        log.info(f'status code is: {r.status_code}')
        log.info(f'response is : {r.text}')
        assert int(validStatusCode) == r.status_code

class API(HttpLocust):
    task_set = APICalls
    # host = 'https://nghttp2.org/httpbin'
    host = baseurl
    min_wait = int(minWait)
    max_wait = int(maxWait)