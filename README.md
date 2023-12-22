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

# Full Documentation
TODO

## function()
### Description
**Returns:** A `type` object
- `param` **[required]**
  - Description
  - Type
  - Valid values
