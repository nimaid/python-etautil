"""A library for tracking, computing, and formatting time estimates."""

__version__ = "2.6.0"

from . import eta, time, constants

# TODO: Add a `statistics_string()` method that is focused on all stats (incl. time taken), not just progress
# TODO: Add eta_bar() wrapper for eta_calc()
# TODO: Move to `etatime` package, make `etautil` just a wrapper for compatibility
