import multiprocessing as mp
import os
from datetime import datetime
from multiprocessing import Process
from random import sample
from time import sleep

from .base import StrategyBase


class FixedTime(StrategyBase):

    def __init__(self, request_fn, workers=1, loadtest_time=30):
        super().__init__(workers)
        self.request_fn = request_fn
        self.loadtest_time = loadtest_time

    def init_inputs(self, raw_payloads):
        return raw_payloads

    def spawn_worker(self, worker_id, inputs, result_queue):
        p = Process(target=self.load_test,
                    args=(worker_id, inputs, result_queue))
        p.start()
        return p

    def join_workers(self):
        sleep(self.loadtest_time)

    def load_test(self, worker_id, payloads_queue: list, result_queue: mp.Queue):
        pid = os.getpid()
        print(f'Worker {worker_id} is starting... pid: {pid}')
        i = 0

        print(f'Worker {worker_id} - Starting to work on queue', flush=True)

        while True:
            try:
                payload = sample(payloads_queue, 1)[0]
                before = datetime.utcnow()
                response = self.request_fn(payload)
                time_delta = datetime.utcnow() - before

                if i % 1000 == 0 or i <= 10:
                    print(f'Worker {worker_id} is running iteration {i}, response={response}',
                          flush=True)

                result_queue.put(
                    (dict(request_time_ms=time_delta.total_seconds() * 1000),
                     worker_id))
            except Exception as e:
                print('error: {}'.format(e))
                result_queue.put(
                    (dict(error=True),
                     worker_id))
            finally:
                i += 1
