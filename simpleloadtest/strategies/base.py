import multiprocessing as mp
from abc import abstractmethod
from datetime import datetime

from .stats import Stats


class StrategyBase:
    def __init__(self, workers):
        self.workers = workers
        self.ps_workers = []

    def start(self, raw_payloads):
        try:
            print('Initializing inputs...')
            inputs = self.init_inputs(raw_payloads)

            print('Starting up workers...')
            before = datetime.utcnow()
            result_queue = mp.Queue()
            for i in range(self.workers):
                p = self.spawn_worker(worker_id=i + 1,
                                      inputs=inputs,
                                      result_queue=result_queue)
                self.ps_workers.append(p)

            self.join_workers()
            total_time_delta = datetime.utcnow() - before
            total_time_seconds = total_time_delta.total_seconds()

            self.terminate_workers()

            times = []
            error_count = 0
            total_requests = 0

            while not result_queue.empty():
                total_requests += 1
                result, pid = result_queue.get()
                if result.get('error'):
                    error_count += 1
                else:
                    times.append(result['request_time_ms'])

            return Stats(workers=self.workers,
                         total_requests=total_requests,
                         total_time_sec=total_time_seconds,
                         times=times,
                         error_count=error_count)
        except Exception as e:
            print(e)
            self.terminate_workers()

    @abstractmethod
    def init_inputs(self, raw_payloads):
        pass

    @abstractmethod
    def spawn_worker(self, worker_id, inputs, result_queue):
        pass

    @abstractmethod
    def join_workers(self):
        pass

    def terminate_workers(self):
        for p in self.ps_workers:
            p.terminate()
