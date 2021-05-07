import json
from abc import ABCMeta, abstractmethod

from utils.const import INVOKE_ITERATOR, INVOKE_SINGLE, INVOKE_CONCURRENT
from utils.time_logger import run_time
from vodka.common.invoker import Invoker


def read_variable(file):
    with open(file, "r") as f:
        variables = json.load(f)
    return [{"name": var, "variable": var} for var in variables]


def post_request(response, result):
    data = str(response.content, 'utf8')
    elements = json.loads(data)['data']
    for ele in elements:
        result[ele] = elements[ele]['result']


class Template(metaclass=ABCMeta):
    def __init__(self, env="dev", file="variable.json"):
        self._variable = read_variable(file)
        self._invoker = Invoker(env, False)
        self._mode = INVOKE_SINGLE
        self._core = 2
        self._limit = None
        self._data = None
        self._filter = None

    def core(self, core):
        self._core = core
        return self

    def limit(self, limit):
        self._limit = limit
        return self

    def iterator(self):
        self._mode = INVOKE_ITERATOR
        return self

    def concurrent(self):
        self._mode = INVOKE_CONCURRENT
        return self

    def filter(self, condition):
        self._filter = condition
        return self

    @run_time
    def run(self):
        data_list = self.load_data()

        if self._filter is not None:
            data_list = list(filter(self._filter, data_list))

        # 条数限制
        if self._limit is not None:
            data_list = data_list[:self._limit]

        params = [self.build_param(data) for data in data_list]
        payloads = [{"params": param, "variables": self._variable} for param in params]

        if self._mode == INVOKE_CONCURRENT:
            # 并发调用
            from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
            pool = ThreadPoolExecutor(max_workers=self._core)
            fs = [pool.submit(self.invoke, i, payload) for i, payload in enumerate(payloads)]
            wait(fs, return_when=ALL_COMPLETED)
            self._data = [f.result() for f in fs]
        else:
            # 递归调用
            self._data = [self.invoke(i, payload) for i, payload in enumerate(payloads)]
        return self

    def invoke(self, index, payload):
        result = {}
        self.pre_request(payload, result)
        response = self._invoker.do_request(payload)
        post_request(response, result)
        print("%d ====> Done" % (index + 1))
        return result

    def pre_request(self, payload, result):
        pass

    @abstractmethod
    def load_data(self) -> list:
        pass

    @abstractmethod
    def build_param(self, param) -> dict:
        pass

    def to_csv(self, file_name="result"):
        import pandas as pd
        df = pd.DataFrame(self._data)
        df.to_csv(file_name + ".csv", index=False)

    def to_sql(self, schema="default"):
        pass
