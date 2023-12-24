# ETA Utility
### A library for tracking, computing, and formatting time estimates in Python.

<p align="center"><a href="https://pypi.org/project/etautil/"><img src="https://pypi.org/static/images/logo-large.9f732b5f.svg" width="200px" alt="etautil on Pypi"></a></p>

## Installation
```commandline
pip install etautil
```

## Basic Usage
```python
import time, random
import etautil


# Just a placeholder function that takes a random amount of time
def process_item(item):
    time.sleep(random.random() * 10)

eta = None  # Initialize here so we can use it later
for item, eta in etautil.eta(range(10)):
    print(eta)  # Print the current progress stats
    process_item(item)

print(f"Done processing {eta.total_items} items in {eta.time_taken_string()}!\n")
```

Here is an example of the sort of output this produces:
```
0.00%
10.00% | 0:00:25 | 11:04:58 AM
20.00% | 0:00:12 | 11:04:45 AM
30.00% | 0:00:29 | 11:05:12 AM
40.00% | 0:00:20 | 11:05:03 AM
50.00% | 0:00:21 | 11:05:11 AM
60.00% | 0:00:18 | 11:05:15 AM
70.00% | 0:00:12 | 11:05:10 AM
80.00% | 0:00:09 | 11:05:14 AM
90.00% | 0:00:04 | 11:05:09 AM
Done processing 10 items in 0:00:35!
```

You can get more verbose information by replacing the for loop with this:
```python
for item, eta in etautil.eta(range(100), verbose=True):
```
Here is an example of the verbose output:
```
0.00% (1/10)
10.00% (2/10) | Time remaining: 1 minute and 14 seconds | ETA: 11:07:24 AM US Mountain Standard Time
20.00% (3/10) | Time remaining: 1 minute and 10 seconds | ETA: 11:07:29 AM US Mountain Standard Time
30.00% (4/10) | Time remaining: 43 seconds | ETA: 11:07:04 AM US Mountain Standard Time
40.00% (5/10) | Time remaining: 37 seconds | ETA: 11:07:03 AM US Mountain Standard Time
50.00% (6/10) | Time remaining: 29 seconds | ETA: 11:06:59 AM US Mountain Standard Time
60.00% (7/10) | Time remaining: 22 seconds | ETA: 11:06:56 AM US Mountain Standard Time
70.00% (8/10) | Time remaining: 17 seconds | ETA: 11:06:58 AM US Mountain Standard Time
80.00% (9/10) | Time remaining: 12 seconds | ETA: 11:07:01 AM US Mountain Standard Time
90.00% (10/10) | Time remaining: 5 seconds | ETA: 11:06:55 AM US Mountain Standard Time
Done processing 10 items in 48 seconds!
```

You can also build a custom message piece-by-piece, like so:
```python
print(f"Processing item: '{item}'")
print(f"  Completed: {eta.percentage_string()}")
print(f"  Time taken: {eta.time_taken_string()}")
print(f"  Time remaining: {eta.time_remaining_string()}")
print(f"  ETA: {eta.eta_string()}")
```
This produces the following output:
```
Processing item: '0'
  Completed: 0.00% (1/10)
  Time taken: 0 seconds
  Time remaining: Not enough data.
  ETA: Not enough data.
Processing item: '1'
  Completed: 10.00% (2/10)
  Time taken: 9 seconds
  Time remaining: 1 minute and 20 seconds
  ETA: 11:41:56 AM US Mountain Standard Time
Processing item: '2'
  Completed: 20.00% (3/10)
  Time taken: 14 seconds
  Time remaining: 56 seconds
  ETA: 11:41:36 AM US Mountain Standard Time
Processing item: '3'
  Completed: 30.00% (4/10)
  Time taken: 19 seconds
  Time remaining: 45 seconds
  ETA: 11:41:31 AM US Mountain Standard Time
Processing item: '4'
  Completed: 40.00% (5/10)
  Time taken: 25 seconds
  Time remaining: 37 seconds
  ETA: 11:41:29 AM US Mountain Standard Time
Processing item: '5'
  Completed: 50.00% (6/10)
  Time taken: 29 seconds
  Time remaining: 29 seconds
  ETA: 11:41:24 AM US Mountain Standard Time
Processing item: '6'
  Completed: 60.00% (7/10)
  Time taken: 34 seconds
  Time remaining: 23 seconds
  ETA: 11:41:23 AM US Mountain Standard Time
Processing item: '7'
  Completed: 70.00% (8/10)
  Time taken: 37 seconds
  Time remaining: 16 seconds
  ETA: 11:41:20 AM US Mountain Standard Time
Processing item: '8'
  Completed: 80.00% (9/10)
  Time taken: 46 seconds
  Time remaining: 11 seconds
  ETA: 11:41:24 AM US Mountain Standard Time
Processing item: '9'
  Completed: 90.00% (10/10)
  Time taken: 49 seconds
  Time remaining: 5 seconds
  ETA: 11:41:21 AM US Mountain Standard Time
```

Each individual property and text field is accessible via public methods.

# Full Documentation
<p align="center"><a href="https://python-etautil.readthedocs.io/en/latest/index.html"><img src="https://brand-guidelines.readthedocs.org/_images/logo-wordmark-vertical-dark.png" width="300px" alt="etautil on Read the Docs"></a></p>
