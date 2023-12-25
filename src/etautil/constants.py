"""Contains constants used in by other components of the module."""
from typing import ClassVar
from dataclasses import dataclass
from pydantic import NonNegativeInt


@dataclass
class EtaDefaults:
    """The defaults to use for the `eta` submodule.

    :cvar bool verbose: If we should make strings verbosely or not.
    :cvar int percent_decimals: The number of decimal places to use in the percentage string.
    :cvar str not_enough_data_string: The string to return when there is not enough data for the desired computation.
    :cvar str sep: The string to use as a seperator between fields.
    """
    verbose: ClassVar[bool] = False
    percent_decimals: ClassVar[NonNegativeInt] = 2
    not_enough_data_string: ClassVar[str] = "not enough data"
    sep: ClassVar[str] = " | "
