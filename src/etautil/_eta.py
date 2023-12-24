import datetime
from pydantic import NonNegativeInt, Field, validate_call
from typing_extensions import Annotated

from ._timestring import TimeString

# TODO: Consider moving back to standard datetime and my own private methods.
# TODO: Add iterable option, so like `for i, eta in etautil.eta(range(100):`

class Eta:
    """Holds ETA state information and provides methods to compute and format time estimate info.

    :param int total_items: The total number of items to process, used in computations.
    :param int current_item_index: The index of the item about to be processed (0-indexed).
    :param pendulum.DateTime start_time: The starting time to use for the computation.
    :param current_time: The time to use for the computation, defaults to the current time.
    :param bool verbose: If we should make strings verbosely or not.
    :param int percent_decimals: The number of decimal places to use in the percentage string.
    :raises pydantic.ValidationError: Raised when a parameter is invalid.
    :raises IndexError: Raised when the index is too large.
    :rtype: Eta
    """
    @validate_call(config={'arbitrary_types_allowed': True})
    def __init__(
            self,
            total_items: Annotated[NonNegativeInt, Field(gt=1)],
            current_item_index: NonNegativeInt,
            start_time: pendulum.DateTime,
            current_time: pendulum.DateTime = None,
            verbose: bool = False,
            percent_decimals: NonNegativeInt = 2
    ):
        if current_time is None:
            current_time = pendulum.now()

        self.total_items = total_items
        self.current_item_index = current_item_index
        self.start_time = start_time
        self.current_time = current_time
        self.verbose = verbose
        self.percent_decimals = percent_decimals

        self._validate_item_index(self.current_item_index)

        if self.verbose:
            self.datetime_format = "dddd, MMMM Do, YYYY @ h:mm:ss A Z"
        else:
            self.datetime_format = "YYYY/MM/DD @ h:mm:ss A"

        self.percent_format = f"{{:.{self.percent_decimals}f}}%"

    def __str__(self) -> str:
        """Returns the string format of this ETA object.

        :return: The user-friendly progress string.
        :rtype: str
        """
        return self.progress_string()

    def _validate_item_index(
            self,
            item_index: NonNegativeInt
    ) -> None:
        """Validate that an index is not larger than the total items and raise an IndexError otherwise.

        Index type and positivity are not validated in this private method because pydantic handles it elsewhere.

        :param int item_index: The index to test.
        :raises IndexError: Raised when the index is too large.
        :rtype: None
        """
        if item_index > self.total_items - 1:
            raise IndexError(f"Item index should be less than {self.total_items - 1} (the total items - 1)")

    def eta(self) -> pendulum.DateTime:
        """Compute the ETA and return it as a pendulum.DateTime object.

        :return: The ETA as a pendulum.DateTime object.
        :rtype: pendulum.DateTime
        """
        return self.current_time + self.time_remaining()

    def eta_string(self) -> str:
        """Compute the ETA and return it as a string.

        :return: The ETA as a human-readable string.
        :rtype: str
        """
        return self.eta().format(self.datetime_format)

    def time_remaining(self) -> pendulum.Duration:
        """Compute the time remaining and return it as a pendulum.Duration object.

        :return: The time remaining as a pendulum.Duration object.
        :rtype: pendulum.Duration
        """
        percent_done = self.percentage()
        progress_scale = (1 - percent_done) / percent_done

        return self.time_taken() * progress_scale

    def time_remaining_string(self) -> str:
        """Compute the time remaining and return it as a string.

        :return: The time remaining as a human-readable string.
        :rtype: str
        """
        return self.time_remaining().in_words()

    def percentage(self) -> float:
        """Compute the completion percentage and return it as a float.

        :return: The completion percentage as a float in range on 0.0 - 1.0.
        :rtype: float
        """
        return self.current_item_index / (self.total_items - 1)

    def percentage_string(self) -> str:
        """Compute the completion percentage and return it as a string.

        :return: The completion percentage as a human-readable string.
        :rtype: str
        """
        percent_string = self.percent_format.format(self.percentage() * 100)
        if self.verbose:
            percent_string += f" ({self.current_item_index + 1}/{self.total_items})"

        return percent_string

    def time_taken(self) -> pendulum.Duration:
        """Compute the time taken and return it as a pendulum.Duration object.

        :return: The time taken as a pendulum.Duration object.
        :rtype: pendulum.Duration
        """
        return self.current_time - self.start_time

    def time_taken_string(self) -> str:
        """Compute the time taken and return it as a pendulum.Duration object.

        :return: The time taken as a pendulum.Duration object.
        :rtype: pendulum.Duration
        """
        return self.time_taken().in_words()

    @validate_call
    def progress_string(
            self,
            sep: str = " | "
    ) -> str:
        percent_string = self.percentage_string()

        if self.current_item_index <= 0:
            return percent_string

        difference_string = self.time_remaining_string()
        eta_string = self.eta_string()
        if self.verbose:
            difference_string = f"Time remaining: {difference_string}"
            eta_string = f"ETA: {eta_string}"

        return sep.join([percent_string, difference_string, eta_string])


class EtaCalculator:
    """Tracks, computes, and formats time estimates.

    :param int total_items: The total number of items to process, used in computations.
    :param pendulum.DateTime start_time: The starting time used in all calculations, defaults to the current time.
    :param bool verbose: If we should make strings verbosely or not.
    :param int percent_decimals: The number of decimal places to use in the percentage string.
    :raises pydantic.ValidationError: Raised when a parameter is invalid.
    :rtype: EtaCalculator
    """
    @validate_call(config={'arbitrary_types_allowed': True})
    def __init__(
            self,
            total_items: Annotated[NonNegativeInt, Field(gt=1)],
            start_time: pendulum.DateTime = None,
            verbose: bool = False,
            percent_decimals: NonNegativeInt = 2
    ):
        if start_time is None:
            start_time = pendulum.now()

        self.total_items = None
        self.set_total_items(total_items)

        self.start_time = None
        self.set_start_time(start_time)

        self.verbose = None
        self.set_verbose(verbose)

        self.percent_decimals = None
        self.set_percent_decimals(percent_decimals)

    def __str__(self) -> str:
        """Returns the string format of this ETA object.

        :return: The user-friendly string representing the calculator object.
        :rtype: str
        """
        return (f"ETA calculator for {self.total_items} items, "
                f"start time = {self.start_time}, "
                f"verbose = {self.verbose}, "
                f"percentage decimal places = {self.percent_decimals}")

    @validate_call(config={'arbitrary_types_allowed': True})
    def get_eta(
            self,
            current_item_index: NonNegativeInt,
            current_time: pendulum.DateTime = None
    ):
        if current_time is None:
            current_time = pendulum.now()

        return Eta(
            total_items=self.total_items,
            current_item_index=current_item_index,
            start_time=self.start_time,
            current_time=current_time,
            verbose=self.verbose,
            percent_decimals=self.percent_decimals
        )

    @validate_call
    def set_total_items(
            self,
            total_items: Annotated[NonNegativeInt, Field(gt=1)]
    ) -> None:
        """Set the total number of items to process.

        :param int total_items: The total number of items to process, used in computations.
        :raises pydantic.ValidationError: Raised when a parameter is invalid.
        :rtype: None
        """
        self.total_items = total_items

    @validate_call(config={'arbitrary_types_allowed': True})
    def set_start_time(
            self,
            start_time: pendulum.DateTime = None
    ) -> None:
        if start_time is None:
            start_time = pendulum.now()

        self.start_time = start_time

    @validate_call
    def set_verbose(
            self,
            verbose: bool
    ) -> None:
        self.verbose = verbose

    @validate_call
    def set_percent_decimals(
            self,
            percent_decimals: NonNegativeInt
    ) -> None:
        self.percent_decimals = percent_decimals
