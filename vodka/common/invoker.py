import datetime
import json

import requests

url_dict = {
    "dev": "http://localhost:20787/vodka/variable/compute",
}

headers = {
    'Content-Type': 'application/json',
    'partner-code': 'Kreditpedia',
    'app-name': 'Kreditpedia_App',
    'partner-key': '786XjbmHO7cdYQr724MG',
}


class Invoker(object):
    def __init__(self, env="dev", log=False):
        self.env = env
        self.log = log
        self.url = url_dict[env]

    def do_request(self, payload):
        if payload is None:
            return
        if payload['params']:
            payload['params']['productName'] = 'pycharm'
            payload['params']['eventId'] = '1_0_17862826732_1548053505007'

        if self.log:
            print(json.dumps(payload, cls=DateEncoder))

        body = json.dumps(payload, default=str, ensure_ascii=False).encode()
        request = requests.request("POST", self.url, headers=headers, data=body)
        return request


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)
