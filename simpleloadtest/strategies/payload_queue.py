import multiprocessing as mp
import os
from datetime import datetime
from multiprocessing import Process
from time import sleep

from .base import StrategyBase


class PayloadQueue(StrategyBase):
    def __init__(self, request_fn, workers=1):
        super().__init__(workers)
        self.request_fn = request_fn
        self.inputs_queue = mp.JoinableQueue()

    def init_inputs(self, raw_payloads):
        for i in raw_payloads:
            self.inputs_queue.put(i)

        return self.inputs_queue

    def spawn_worker(self, worker_id, inputs, result_queue):
        p = Process(target=self.load_test,
                    args=(worker_id, inputs, result_queue))
        p.start()
        return p

    def join_workers(self):
        self.inputs_queue.join()
        sleep(0.5)

    def load_test(self, worker_id, payloads_queue: mp.Queue, result_queue: mp.Queue):
        pid = os.getpid()
        print(f'Worker {worker_id} is starting... pid: {pid}')
        i = 0

        print(f'Worker {worker_id} - Starting to work on queue', flush=True)

        while True:
            try:
                payload = payloads_queue.get()
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
                payloads_queue.task_done()
