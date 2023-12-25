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
from etautil.eta import eta_calculator


# Just a placeholder function that takes a random amount of time
def process_item(item):
    time.sleep(random.random() * 20)


for item, eta in eta_calculator(range(10)):  # Creates a new etautil.Eta object for each item
    print(eta)  # Print the current progress stats
    process_item(item)  # Do your processing here
```
If you want to access the eta stats outside the loop, you can use this pattern to do so:
```python
eta = None  # Initialize the eta variable here, so we can use it outside the loop
for item, eta in eta_calculator(range(10)):
    print(eta)
    process_item(item)
eta.complete()  # Update the last created etautil.Eta object to completed, using now as the end time

print(f"Done processing {eta.total_items} items in {eta.time_taken_string}!\n")
```

Here is an example of the sort of output this produces:
```
0.00%
10.00% | 0:01:33 | 12:25:16 AM
20.00% | 0:01:56 | 12:25:57 AM
30.00% | 0:01:13 | 12:25:16 AM
40.00% | 0:00:55 | 12:25:03 AM
50.00% | 0:00:55 | 12:25:22 AM
60.00% | 0:00:43 | 12:25:18 AM
70.00% | 0:00:32 | 12:25:19 AM
80.00% | 0:00:19 | 12:25:09 AM
90.00% | 0:00:09 | 12:25:00 AM
Done processing 10 items in 0:01:33!
```

You can get more verbose information by replacing the for loop with this:

```python
for item, eta in eta_calculator(range(10), verbose=True):
```
Here is an example of the verbose output:
```
0.00% (0/10)
10.00% (1/10) | Time remaining: 1 minute and 54 seconds | ETA: 12:27:33 AM US Mountain Standard Time
20.00% (2/10) | Time remaining: 1 minute and 33 seconds | ETA: 12:27:22 AM US Mountain Standard Time
30.00% (3/10) | Time remaining: 1 minute and 7 seconds | ETA: 12:27:02 AM US Mountain Standard Time
40.00% (4/10) | Time remaining: 50 seconds | ETA: 12:26:49 AM US Mountain Standard Time
50.00% (5/10) | Time remaining: 51 seconds | ETA: 12:27:08 AM US Mountain Standard Time
60.00% (6/10) | Time remaining: 41 seconds | ETA: 12:27:09 AM US Mountain Standard Time
70.00% (7/10) | Time remaining: 28 seconds | ETA: 12:27:01 AM US Mountain Standard Time
80.00% (8/10) | Time remaining: 20 seconds | ETA: 12:27:05 AM US Mountain Standard Time
90.00% (9/10) | Time remaining: 10 seconds | ETA: 12:27:07 AM US Mountain Standard Time
Done processing 10 items in 1 minute and 51 seconds!
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
  Time taken: 11 seconds
  Time remaining: 1 minute and 38 seconds
  ETA: 12:29:31 AM US Mountain Standard Time
Processing item: '2'
  Completed: 20.00% (2/10)
  Time taken: 29 seconds
  Time remaining: 1 minute and 55 seconds
  ETA: 12:30:05 AM US Mountain Standard Time
Processing item: '3'
  Completed: 30.00% (3/10)
  Time taken: 47 seconds
  Time remaining: 1 minute and 50 seconds
  ETA: 12:30:18 AM US Mountain Standard Time
Processing item: '4'
  Completed: 40.00% (4/10)
  Time taken: 54 seconds
  Time remaining: 1 minute and 21 seconds
  ETA: 12:29:57 AM US Mountain Standard Time
Processing item: '5'
  Completed: 50.00% (5/10)
  Time taken: 56 seconds
  Time remaining: 56 seconds
  ETA: 12:29:33 AM US Mountain Standard Time
Processing item: '6'
  Completed: 60.00% (6/10)
  Time taken: 1 minute and 3 seconds
  Time remaining: 42 seconds
  ETA: 12:29:27 AM US Mountain Standard Time
Processing item: '7'
  Completed: 70.00% (7/10)
  Time taken: 1 minute and 22 seconds
  Time remaining: 35 seconds
  ETA: 12:29:38 AM US Mountain Standard Time
Processing item: '8'
  Completed: 80.00% (8/10)
  Time taken: 1 minute and 28 seconds
  Time remaining: 22 seconds
  ETA: 12:29:32 AM US Mountain Standard Time
Processing item: '9'
  Completed: 90.00% (9/10)
  Time taken: 1 minute and 48 seconds
  Time remaining: 12 seconds
  ETA: 12:29:41 AM US Mountain Standard Time
Done processing 10 items in 1 minute and 57 seconds!
```

# Full Documentation
<p align="center"><a href="https://python-etautil.readthedocs.io/en/latest/index.html"><img src="https://brand-guidelines.readthedocs.org/_images/logo-wordmark-vertical-dark.png" width="300px" alt="etautil on Read the Docs"></a></p>
