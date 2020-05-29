from collections import OrderedDict
from itertools import product
import multiprocessing as mp
import numpy as np
import pickle
import gc


class BackTester:
    def __init__(self, max_results_keep = 200):
        self.callback_func = self.nothing
        self.results_func = None
        self.max_results_keep = max_results_keep
        self._params = []
        self._range_params = []
        self._results = OrderedDict()

    def build_params(self, **params):
        self._keys = list(params.keys())
        self._total = 1
                
        for param in self._keys.copy():
            item = params[param]
            if any([(type(item) == range),
                    (type(item) == np.ndarray),
                    (type(item) == list),
            ]):
                self._range_params.append(list(item))
                self._total*=int(len(list(item)))
            else:
                self._range_params.append([item])
    
    @property
    def params(self):
        return self._params

    @property
    def total(self):
        return self._total

    def get_item_dict_from_tuple(self, item):
        item_dict = {}
        for index, key in enumerate(self._keys):
            item_dict[key] = item[index]
        return item_dict

    def handle_results(self, index):
        if not self.results_func is None and (len(self._results)>=self.max_results_keep):
            self.results_func(self._results, index+1, self.total)
            self._results = {}

    def run(self):
        for index, item_tuple in enumerate(product(*self._range_params)):
            item = self.get_item_dict_from_tuple(item_tuple)
            try:
                self._results[index] = self.callback_func(**item)
                self._results[index]["_status"] = "OK"
            except Exception as e:
                self._results[index] = {}
                self._results[index]["_status"] = "error"
                self._results[index]["_status_msg"] = str(e)

            self.handle_results(index)
        
        if not self.results_func is None:
            self.results_func(self._results, index+1, self.total)

        return self._results

    def callback(self, callback_func):
        self.callback_func = callback_func

    def nothing(self, **kwargs):
        """default callback """
        return {"nothing": "should be set a callback function"}

    def callback_results(self, results_func):
        self.results_func = results_func

    def run_mp(self, cpus=2):
        jobs = []
        mp.set_start_method('spawn')
        ctx = mp.get_context('spawn')
        results_q = ctx.Queue()
        functions_q = ctx.Queue()
        for index, item_tuple in enumerate(product(*self._range_params)):
            item = self.get_item_dict_from_tuple(item_tuple)
            functions_q.put({"_index": index,
                    "_function": pickle.dumps(self.callback_func),
                    "_params": item,
                })
            p = ctx.Process(target=handle_mp_target, 
                    args=(functions_q, results_q))
            p.start()
            jobs.append(p)
            if len(jobs)>=cpus:
                for j in jobs:
                    j.join()
                jobs = []
            while not results_q.empty():
                item = results_q.get()
                self._results[item["_index"]] = item["_result"]

            self.handle_results(index)

        if not self.results_func is None:
            self.results_func(self._results, index+1, self.total)

        return self._results


def handle_mp_target(functions, results):
    """default callback """
    item = functions.get()
    function_ = pickle.loads(item["_function"])
    result = function_(**item["_params"])
    results.put({"_index": item["_index"],
        "_result": result
    })
