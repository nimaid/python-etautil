# ETA Utility
### A library of tools for tracking, computing, and formatting time estimates.

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
1.59% | 0:38:43 | 3:34:32 PM
1.60% | 0:38:43 | 3:34:32 PM
1.61% | 0:38:43 | 3:34:32 PM
1.61% | 0:38:42 | 3:34:32 PM
1.62% | 0:38:42 | 3:34:32 PM
1.63% | 0:38:42 | 3:34:32 PM
1.64% | 0:38:42 | 3:34:32 PM
1.65% | 0:38:42 | 3:34:32 PM
1.65% | 0:38:42 | 3:34:32 PM
1.66% | 0:38:42 | 3:34:32 PM
...
```

You can get more verbose information by doing:
```python
eta = Eta(item_count, verbose=True)
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
