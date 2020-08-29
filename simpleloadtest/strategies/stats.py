import numpy as np


class Stats:
    def __init__(self, workers, total_requests, total_time_sec, times, error_count):
        self.workers = workers
        self.total_requests = total_requests
        self.total_time_sec = total_time_sec
        self.times = times
        self.error_count = error_count

    def print(self):
        print('----' * 5)
        print(f'Done! Took {self.total_time_sec} seconds')
        print(f'Number of invokes: {self.total_requests}; Number of workers: {self.workers}')
        err_rate = round(self.error_count / self.total_requests * 100, 2)
        print(f'Error rate: {err_rate}% ({self.error_count}/{self.total_requests})')
        throughput = self.total_requests / self.total_time_sec
        print(f'Throughput: {throughput} req/sec')

        print('----' * 5)
        print(f'Max: {np.percentile(self.times, 100)}ms')
        print(f'Min: {np.percentile(self.times, 0)}ms')
        print(f'Average: {np.average(self.times)}ms')
        print(f'Median: {np.percentile(self.times, 50)}ms')
        print(f'Upper 90: {np.percentile(self.times, 90)}ms')
        print(f'Upper 99: {np.percentile(self.times, 99)}ms')
        print(f'STD: {np.std(self.times)}')
        print('----' * 10)
        print('----' * 10)
        print()
