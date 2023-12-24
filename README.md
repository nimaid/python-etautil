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
    time.sleep(random.random() * 5)

eta = None  # Initialize here so we can use it later
for item, eta in etautil.eta(range(100)):
    print(eta)  # Print the current progress stats
    process_item(item)

print(f"Done processing {eta.total_items} items in {eta.time_taken_string()}!\n")
```

Here is an example of the sort of output this produces:
```
0.00%
1.00% | 0:03:40 | 10:49:34 AM
2.00% | 0:04:32 | 10:50:29 AM
3.00% | 0:05:19 | 10:51:22 AM
4.00% | 0:05:54 | 10:52:01 AM
5.00% | 0:05:38 | 10:51:48 AM
6.00% | 0:05:53 | 10:52:08 AM
7.00% | 0:06:02 | 10:52:21 AM
8.00% | 0:05:41 | 10:52:03 AM
9.00% | 0:05:09 | 10:51:32 AM
...
```

You can get more verbose information by replacing the for loop with this:
```python
for item, eta in etautil.eta(range(100), verbose=True):
```
Here is an example of the verbose output:
```
0.00% (1/100)
1.00% (2/100) | Time remaining: 6 minutes and 35 seconds | ETA: 10:51:05 AM US Mountain Standard Time
2.00% (3/100) | Time remaining: 4 minutes and 17 seconds | ETA: 10:48:49 AM US Mountain Standard Time
3.00% (4/100) | Time remaining: 5 minutes and 28 seconds | ETA: 10:50:05 AM US Mountain Standard Time
4.00% (5/100) | Time remaining: 5 minutes and 58 seconds | ETA: 10:50:39 AM US Mountain Standard Time
5.00% (6/100) | Time remaining: 4 minutes and 58 seconds | ETA: 10:49:40 AM US Mountain Standard Time
6.00% (7/100) | Time remaining: 5 minutes and 15 seconds | ETA: 10:50:02 AM US Mountain Standard Time
7.00% (8/100) | Time remaining: 4 minutes and 56 seconds | ETA: 10:49:45 AM US Mountain Standard Time
8.00% (9/100) | Time remaining: 4 minutes and 18 seconds | ETA: 10:49:07 AM US Mountain Standard Time
9.00% (10/100) | Time remaining: 4 minutes and 21 seconds | ETA: 10:49:13 AM US Mountain Standard Time
...
```

Each individual property and text field is accessible via public methods.

# Full Documentation
<p align="center"><a href="https://python-etautil.readthedocs.io/en/latest/index.html"><img src="https://brand-guidelines.readthedocs.org/_images/logo-wordmark-vertical-dark.png" width="300px" alt="etautil on Read the Docs"></a></p>
