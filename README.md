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
...
1.59% | 38M:43S | 3:34:32 PM
1.60% | 38M:43S | 3:34:32 PM
1.61% | 38M:43S | 3:34:32 PM
1.61% | 38M:42S | 3:34:32 PM
1.62% | 38M:42S | 3:34:32 PM
1.63% | 38M:42S | 3:34:32 PM
1.64% | 38M:42S | 3:34:32 PM
1.65% | 38M:42S | 3:34:32 PM
1.65% | 38M:42S | 3:34:32 PM
1.66% | 38M:42S | 3:34:32 PM
...
```

You can get more verbose information by doing:
```python
eta = Eta(item_count, verbose=True)
```
... or change the verbosity at any time with:
```python
eta.set_verbose(True)
```
Here is an example of the verbose output:
```
...
2.10% (264/12518) | Time remaining: 39 minutes and 25 seconds | ETA: 3:40:33 PM
2.11% (265/12518) | Time remaining: 39 minutes and 25 seconds | ETA: 3:40:33 PM
2.12% (266/12518) | Time remaining: 39 minutes and 25 seconds | ETA: 3:40:33 PM
2.13% (267/12518) | Time remaining: 39 minutes and 24 seconds | ETA: 3:40:33 PM
2.13% (268/12518) | Time remaining: 39 minutes and 24 seconds | ETA: 3:40:33 PM
2.14% (269/12518) | Time remaining: 39 minutes and 24 seconds | ETA: 3:40:33 PM
2.15% (270/12518) | Time remaining: 39 minutes and 23 seconds | ETA: 3:40:32 PM
2.16% (271/12518) | Time remaining: 39 minutes and 23 seconds | ETA: 3:40:32 PM
2.17% (272/12518) | Time remaining: 39 minutes and 23 seconds | ETA: 3:40:32 PM
2.17% (273/12518) | Time remaining: 39 minutes and 23 seconds | ETA: 3:40:32 PM
...
```

Each individual property and text field is accessible via public methods.

# Full Documentation
<p align="center"><a href="https://python-etautil.readthedocs.io/en/latest/index.html"><img src="https://brand-guidelines.readthedocs.org/_images/logo-wordmark-vertical-dark.png" width="300px" alt="etautil on Read the Docs"></a></p>
