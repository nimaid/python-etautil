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
    :cvar str invalid_string_type_string: The string to return when Eta.string() is given a bad string type.
    """
    verbose: ClassVar[bool] = False
    percent_decimals: ClassVar[NonNegativeInt] = 2
    not_enough_data_string: ClassVar[str] = "not enough data"
    sep: ClassVar[str] = " | "
    invalid_string_type_string = "invalid string type requested"


@dataclass
class TimeDefaults:
    """The defaults to use for the `time` submodule.

    :cvar str unknown_format_string: The string to use when an unknown format is passed to TimeString.automatic().
    """
    unknown_format_string: ClassVar[str] = "unknown time format"
