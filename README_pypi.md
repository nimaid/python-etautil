# ETA Utility
### A library for tracking, computing, and formatting time estimates.

## Basic Usage
```python
import time, random
import etautil


# Just a placeholder function that takes a random amount of time
def process_item(item):
    time.sleep(random.random() * 20)

eta = None  # Initialize here so we can use it later
for item, eta in etautil.eta(range(10)):
    print(eta)  # Print the current progress stats
    process_item(item)

print(f"Done processing {eta.total_items} items in {eta.time_taken_string}!\n")
```

Here is an example of the sort of output this produces:
```
0.00%
10.00% | 0:00:13 | 12:04:01 PM
20.00% | 0:01:10 | 12:05:15 PM
30.00% | 0:01:16 | 12:05:34 PM
40.00% | 0:00:52 | 12:05:13 PM
50.00% | 0:00:47 | 12:05:21 PM
60.00% | 0:00:44 | 12:05:35 PM
70.00% | 0:00:29 | 12:05:24 PM
80.00% | 0:00:21 | 12:05:32 PM
90.00% | 0:00:11 | 12:05:37 PM
Done processing 10 items in 0:01:39!
```

You can get more verbose information by replacing the for loop with this:
```python
for item, eta in etautil.eta(range(10), verbose=True):
```
Here is an example of the verbose output:
```
0.00% (0/10)
10.00% (1/10) | Time remaining: 1 minute and 45 seconds | ETA: 12:03:37 PM US Mountain Standard Time
20.00% (2/10) | Time remaining: 1 minute and 22 seconds | ETA: 12:03:22 PM US Mountain Standard Time
30.00% (3/10) | Time remaining: 1 minute and 3 seconds | ETA: 12:03:10 PM US Mountain Standard Time
40.00% (4/10) | Time remaining: 1 minute and 7 seconds | ETA: 12:03:31 PM US Mountain Standard Time
50.00% (5/10) | Time remaining: 56 seconds | ETA: 12:03:32 PM US Mountain Standard Time
60.00% (6/10) | Time remaining: 43 seconds | ETA: 12:03:27 PM US Mountain Standard Time
70.00% (7/10) | Time remaining: 28 seconds | ETA: 12:03:12 PM US Mountain Standard Time
80.00% (8/10) | Time remaining: 21 seconds | ETA: 12:03:23 PM US Mountain Standard Time
90.00% (9/10) | Time remaining: 10 seconds | ETA: 12:03:19 PM US Mountain Standard Time
Done processing 10 items in 1 minute and 29 seconds!
```

You can also build a custom message piece-by-piece, like so:

```python
print(f"Processing item: '{item}'")
print(f"  Completed: {eta.percentage_string}")
print(f"  Time taken: {eta.time_taken_string}")
print(f"  Time remaining: {eta.time_remaining_string}")
print(f"  ETA: {eta.eta_string}")
```
This produces the following output:
```
Processing item: '0'
  Completed: 0.00% (0/10)
  Time taken: 0 seconds
  Time remaining: not enough data
  ETA: not enough data
Processing item: '1'
  Completed: 10.00% (1/10)
  Time taken: 18 seconds
  Time remaining: 2 minutes and 39 seconds
  ETA: 12:10:19 PM US Mountain Standard Time
Processing item: '2'
  Completed: 20.00% (2/10)
  Time taken: 37 seconds
  Time remaining: 2 minutes and 28 seconds
  ETA: 12:10:28 PM US Mountain Standard Time
Processing item: '3'
  Completed: 30.00% (3/10)
  Time taken: 49 seconds
  Time remaining: 1 minute and 55 seconds
  ETA: 12:10:07 PM US Mountain Standard Time
Processing item: '4'
  Completed: 40.00% (4/10)
  Time taken: 1 minute and 4 seconds
  Time remaining: 1 minute and 36 seconds
  ETA: 12:10:03 PM US Mountain Standard Time
Processing item: '5'
  Completed: 50.00% (5/10)
  Time taken: 1 minute and 22 seconds
  Time remaining: 1 minute and 22 seconds
  ETA: 12:10:06 PM US Mountain Standard Time
Processing item: '6'
  Completed: 60.00% (6/10)
  Time taken: 1 minute and 42 seconds
  Time remaining: 1 minute and 8 seconds
  ETA: 12:10:12 PM US Mountain Standard Time
Processing item: '7'
  Completed: 70.00% (7/10)
  Time taken: 1 minute and 43 seconds
  Time remaining: 44 seconds
  ETA: 12:09:50 PM US Mountain Standard Time
Processing item: '8'
  Completed: 80.00% (8/10)
  Time taken: 1 minute and 51 seconds
  Time remaining: 28 seconds
  ETA: 12:09:41 PM US Mountain Standard Time
Processing item: '9'
  Completed: 90.00% (9/10)
  Time taken: 1 minute and 56 seconds
  Time remaining: 13 seconds
  ETA: 12:09:31 PM US Mountain Standard Time
Done processing 10 items in 1 minute and 56 seconds!
```

# Full Documentation
<p align="center"><a href="https://python-etautil.readthedocs.io/en/latest/index.html"><img src="https://brand-guidelines.readthedocs.org/_images/logo-wordmark-vertical-dark.png" width="300px" alt="etautil on Read the Docs"></a></p>
