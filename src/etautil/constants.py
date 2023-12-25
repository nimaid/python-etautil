from dataclasses import dataclass


@dataclass
class Defaults:
    verbose = False
    percent_decimals = 2
    not_enough_data_string = "not enough data"
    sep = " | "
