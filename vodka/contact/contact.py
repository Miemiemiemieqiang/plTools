import json

import pandas as pd

from vodka.common.template import Template


class Contact(Template):
    def __init__(self, env="dev"):
        super().__init__(env=env)

    def load_data(self):
        df = pd.read_csv('../../data/contact/test_data0506.csv')
        data_list = [row for _, row in df.iterrows()]
        return data_list

    def build_param(self, param) -> dict:
        return build_param(param)

    def pre_request(self, payload, result):
        result["order_id"] = payload['params']["orderId"]


def build_param(param) -> dict:
    data = {}
    emers = json.loads(param['emergency_info'])
    target = [
        {'name': emer['emergencyName'], 'phone': emer['emergencyPhone'], 'relation': emer['emergencyRelation']}
        for emer in emers]
    data["userEmerContacts"] = target
    data["deviceInfo"] = {}
    data["deviceInfo"]['contact'] = json.loads(param['contact'])
    return dict(machineReviewInput=json.dumps(data), orderId=param['order_id'])


if __name__ == '__main__':
    context = Contact()
    context.iterator().limit(1).core(2).run().to_csv()
