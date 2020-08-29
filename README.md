# simple-loadtest

Used for creating a simple load tests with python

## Fixed Time Load Test
Runs the load-test for a fixed amount of time

```python
from simpleloadtest import FixedTime

def req(payload):
    res = requests.post(URL, json=payload)
    return res.json()


def main():
    s = FixedTime(request_fn=req,
                  workers=5,
                  loadtest_time=10)

    payloads = [dict(i=i) for i in range(100)]
    stats = s.start(payloads)
    stats.print()

if __name__ == '__main__':
    main()
```

## Payload Queue Load Test
Runs the load-test until all the payloads have been sent.

```python
from simpleloadtest import PayloadQueue

def req(payload):
    res = requests.post(URL, json=payload)
    return res.json()


def main():
    s = PayloadQueue(request_fn=req,
                     workers=5)

    payloads = [dict(i=i) for i in range(100)]
    stats = s.start(payloads)
    stats.print()

if __name__ == '__main__':
    main()
```

## Stats output
```
--------------------
Done! Took 10.021683 seconds
Number of invokes: 97; Number of workers: 5
Error rate: 0.0% (0/97)
Throughput: 9.679012996120512 req/sec
--------------------
Max: 501.077ms
Min: 500.031ms
Average: 500.3540309278351ms
Median: 500.13300000000004ms
Upper 90: 501.0534ms
Upper 99: 501.07508ms
STD: 0.3806369445804648
----------------------------------------
----------------------------------------

```