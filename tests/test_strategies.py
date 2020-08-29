import unittest
from time import sleep

from simpleloadtest import FixedTime, PayloadQueue
from tests.utils import capture_output


class StrategiesTest(unittest.TestCase):

    def setUp(self):
        self.payloads = list(range(10))

    @staticmethod
    def req_fn(payload):
        sleep(0.01)

    def test_fixed_time(self):
        with capture_output() as _:
            test_time = 2
            stats = FixedTime(request_fn=self.req_fn,
                              loadtest_time=test_time).start(self.payloads)

            delta = abs(stats.total_time_sec - test_time)
            self.assertLess(delta, 1)

    def test_payload_queue(self):
        # with capture_output() as _:
        stats = PayloadQueue(request_fn=self.req_fn).start(self.payloads)

        self.assertEqual(stats.total_requests, len(self.payloads))
