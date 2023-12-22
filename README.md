# ETA Utility
### A simple abstraction for computing and formatting time estimates.

## Basic Usage
```python
from etautil import Eta

item_count = 10000

print(f"Processing {item_count} items...")

eta = Eta(item_count)  # Starts keeping time now
for item in range(item_count):
    print(eta.get_progress_string(item))  # Print the current progress stats
    ...  # Do something

print(f"Done processing {item_count} items in {eta.get_time_taken_string()}!\n")
```

Here is an example of the sort of output this produces:
```
...
1.59% | 0H:38M:43S | 3:34:32 PM
1.60% | 0H:38M:43S | 3:34:32 PM
1.61% | 0H:38M:43S | 3:34:32 PM
1.61% | 0H:38M:42S | 3:34:32 PM
1.62% | 0H:38M:42S | 3:34:32 PM
1.63% | 0H:38M:42S | 3:34:32 PM
1.64% | 0H:38M:42S | 3:34:32 PM
1.65% | 0H:38M:42S | 3:34:32 PM
1.65% | 0H:38M:42S | 3:34:32 PM
1.66% | 0H:38M:42S | 3:34:32 PM
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
TODO

## function()
### Description
**Returns:** A `type` object
- `param` **[required]**
  - Description
  - Type
  - Valid values
