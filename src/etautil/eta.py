"""Provides tools for tracking, computing, and formatting time estimates."""
import datetime
from dataclasses import dataclass
from typing import Any, Annotated, Iterator, Sequence
from pydantic import NonNegativeInt, Field, validate_call

from .time import TimeString
from .constants import EtaDefaults

# TODO: Add a `statistics_string()` method that is focused on all stats (incl. time taken), not just progress
# TODO: Add eta_bar() wrapper for eta_calc()
# TODO: Move to `etatime` package, make `etautil` just a wrapper for compatibility


class Eta:
    """Data class to hold, compute, and format ETA state information and time estimate info.

    :param int total_items: The total number of items to process, used in computations.
    :param int item_index: The index of the item about to be processed (0-indexed).
    :param datetime.datetime start_time: The starting time to use for the computation.
    :param current_time: The time to use for the computation, defaults to the current time.
    :param bool verbose: If we should make strings verbosely or not.
    :param int percent_decimals: The number of decimal places to use in the percentage string.
    :param str not_enough_data_string: The string to return when there is not enough data for the desired computation.

    :ivar int total_items: The total number of items to process, used in computations.
    :ivar int item_index: The index of the item about to be processed (0-indexed).
    :ivar datetime.datetime start_time: The starting time to use for the computation.
    :ivar current_time: The time to use for the computation, defaults to the current time.
    :ivar bool verbose: If we should make strings verbosely or not.
    :ivar int percent_decimals: The number of decimal places to use in the percentage string.
    :ivar str not_enough_data_string: The string to return when there is not enough data for the desired computation.

    :ivar datetime.datetime eta: The estimated completion time.
    :ivar datetime.timedelta time_remaining: The time remaining.
    :ivar float percentage: The completion percentage.
    :ivar datetime.timedelta time_taken: The time taken.
    :ivar str eta_string: The estimated completion time as a human-readable sting.
    :ivar str time_remaining_string: The time remaining as a human-readable string.
    :ivar str percentage_string: The completion percentage as a human-readable string.
    :ivar str time_taken_string: The time taken as a human-readable string.

    :raises pydantic.ValidationError: Raised when a parameter is invalid.
    :raises IndexError: Raised when the index is too large.
    """
    @validate_call
    def __init__(
            self,
            total_items: Annotated[NonNegativeInt, Field(gt=1)],
            item_index: NonNegativeInt,
            start_time: datetime.datetime,
            current_time: datetime.datetime = None,
            verbose: bool = EtaDefaults.verbose,
            percent_decimals: NonNegativeInt = EtaDefaults.percent_decimals,
            not_enough_data_string: str = EtaDefaults.not_enough_data_string
    ):
        if current_time is None:
            current_time = datetime.datetime.now()

        self.total_items = total_items
        self.item_index = item_index
        self.start_time = start_time
        self.current_time = current_time
        self.verbose = verbose
        self.percent_decimals = percent_decimals
        self.not_enough_data_string = not_enough_data_string

        self._validate_item_index(self.item_index)

        self.percent_format = f"{{:.{self.percent_decimals}f}}%"

        self.eta = self._eta()
        self.eta_string = self._eta_string()
        self.time_remaining = self._time_remaining()
        self.time_remaining_string = self._time_remaining_string()
        self.percentage = self._percentage()
        self.percentage_string = self._percentage_string()
        self.time_taken = self._time_taken()
        self.time_taken_string = self._time_taken_string()


    def __str__(self) -> str:
        """Returns the string format of this ETA object.

        :return: The user-friendly progress string.
        :rtype: str
        """
        return self.progress_string()

    def __repr__(self) -> str:
        """Returns the string format of this ETA object.

        :return: The user-friendly progress string.
        :rtype: str
        """
        return self.__str__()

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

    def _eta(self) -> datetime.datetime | None:
        """Compute the ETA and return it as a datetime.datetime object.

        :return: The ETA as a datetime.datetime object.
        :rtype: datetime.datetime
        """
        time_remaining = self._time_remaining()
        if time_remaining is None:
            return None

        return self.current_time + time_remaining

    def _eta_string(self) -> str:
        """Compute the ETA and return it as a string.

        :return: The ETA as a human-readable string.
        :rtype: str
        """
        if self.eta is None:
            return self.not_enough_data_string

        if self.verbose:
            return TimeString.DateTime.long(self.eta)

        return TimeString.DateTime.short(self.eta)

    def _time_remaining(self) -> datetime.timedelta | None:
        """Compute the time remaining and return it as a datetime.timedelta object.

        :return: The time remaining as a datetime.timedelta object, None if the index is 0.
        :rtype: datetime.timedelta | None
        """
        percent_done = self._percentage()
        if percent_done <= 0:
            return None

        progress_scale = (1 - percent_done) / percent_done

        return self._time_taken() * progress_scale

    def _time_remaining_string(self) -> str:
        """Compute the time remaining and return it as a string.

        :return: The time remaining as a human-readable string.
        :rtype: str
        """
        if self.time_remaining is None:
            return self.not_enough_data_string

        if self.verbose:
            return TimeString.TimeDelta.long(self.time_remaining)

        return TimeString.TimeDelta.short(self.time_remaining)

    def _percentage(self) -> float:
        """Compute the completion percentage and return it as a float.

        :return: The completion percentage as a float in range on 0.0 - 1.0.
        :rtype: float
        """
        return self.item_index / self.total_items

    def _percentage_string(self) -> str:
        """Compute the completion percentage and return it as a string.

        :return: The completion percentage as a human-readable string.
        :rtype: str
        """
        percent_string = self.percent_format.format(self.percentage * 100)
        if self.verbose:
            percent_string += f" ({self.item_index}/{self.total_items})"

        return percent_string

    def _time_taken(self) -> datetime.timedelta:
        """Compute the time taken and return it as a datetime.timedelta object.

        :return: The time taken as a datetime.timedelta object.
        :rtype: datetime.timedelta
        """
        return self.current_time - self.start_time

    def _time_taken_string(self) -> str:
        """Compute the time taken and return it as a string.

        :return: The time taken as a datetime.timedelta object.
        :rtype: str
        """
        if self.verbose:
            return TimeString.TimeDelta.long(self.time_taken)

        return TimeString.TimeDelta.short(self.time_taken)

    @validate_call
    def progress_string(
            self,
            sep: str = EtaDefaults.sep
    ) -> str:
        """Combine the most useful stats into a string focused on conveying progress and return it.

        :param str sep: The string to use as a seperator between fields.

        :raises pydantic.ValidationError: Raised when a parameter is invalid.

        :return: A human-readable string that includes (in order) percentage, time remaining, and ETA.
        :rtype: str
        """
        percent_string = self._percentage_string()

        if self.item_index <= 0:
            return percent_string

        difference_string = self._time_remaining_string()
        eta_string = self._eta_string()
        if self.verbose:
            difference_string = f"Time remaining: {difference_string}"
            eta_string = f"ETA: {eta_string}"

        return sep.join([percent_string, difference_string, eta_string])

    @validate_call
    def complete(
            self,
            current_time: datetime.datetime = None,
    ) -> None:
        """Set the ETA item to completed (100%).

        :param datetime.datetime current_time: The time to use for the computation, defaults to the current time.

        :rtype: None
        """
        if current_time is None:
            current_time = datetime.datetime.now()

        self.item_index = self.total_items
        self.current_time = current_time

        self.eta = current_time
        self.eta_string = self._eta_string()
        self.time_remaining = datetime.timedelta(0)
        self.time_remaining_string = self._time_remaining_string()
        self.percentage = self._percentage()
        self.percentage_string = self._percentage_string()
        self.time_taken = self._time_taken()
        self.time_taken_string = self._time_taken_string()


class EtaCalculator:
    """Tracks, computes, and formats time estimates.

    :param int total_items: The total number of items to process, used in computations.
    :param datetime.datetime start_time: The starting time used in all calculations, defaults to the current time.
    :param bool verbose: If we should make strings verbosely or not.
    :param int percent_decimals: The number of decimal places to use in the percentage string.
    :param str not_enough_data_string: The string to return when there is not enough data for the desired computation.

    :ivar int total_items: The total number of items to process, used in computations.
    :ivar datetime.datetime start_time: The starting time used in all calculations, defaults to the current time.
    :ivar bool verbose: If we should make strings verbosely or not.
    :ivar int percent_decimals: The number of decimal places to use in the percentage string.
    :ivar str not_enough_data_string: The string to return when there is not enough data for the desired computation.

    :raises pydantic.ValidationError: Raised when a parameter is invalid.
    """
    @validate_call
    def __init__(
            self,
            total_items: Annotated[NonNegativeInt, Field(gt=1)],
            start_time: datetime.datetime = None,
            verbose: bool = EtaDefaults.verbose,
            percent_decimals: NonNegativeInt = EtaDefaults.percent_decimals,
            not_enough_data_string: str = EtaDefaults.not_enough_data_string
    ):
        if start_time is None:
            start_time = datetime.datetime.now()

        self.total_items = None
        self.set_total_items(total_items)

        self.start_time = None
        self.set_start_time(start_time)

        self.verbose = None
        self.set_verbose(verbose)

        self.percent_decimals = None
        self.set_percent_decimals(percent_decimals)

        self.not_enough_data_string = None
        self.set_not_enough_data_string(not_enough_data_string)

    def __str__(self) -> str:
        """Return the string format of this ETA calculator object.

        :return: The user-friendly string representing the calculator object.
        :rtype: str
        """
        return (f"ETA calculator for {self.total_items} items, "
                f"start time = {self.start_time}, "
                f"verbose = {self.verbose}, "
                f"percentage decimal places = {self.percent_decimals}")

    def __repr__(self) -> str:
        """Return the string format of this ETA calculator object.

        :return: The user-friendly string representing the calculator object.
        :rtype: str
        """
        return self.__str__()

    @validate_call
    def get_eta(
            self,
            item_index: NonNegativeInt,
            current_time: datetime.datetime = None
    ) -> Eta:
        """Get the current ETA calculation and return it as an Eta object.

        :param int item_index: The index of the item about to be processed (0-indexed).
        :param datetime.datetime current_time: The time to use for the computation, defaults to the current time.

        :raises pydantic.ValidationError: Raised when a parameter is invalid.
        :raises IndexError: Raised when the index is too large.

        :return: The current ETA calculation as an Eta object.
        :rtype: Eta
        """
        if current_time is None:
            current_time = datetime.datetime.now()

        return Eta(
            total_items=self.total_items,
            item_index=item_index,
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

    @validate_call
    def set_start_time(
            self,
            start_time: datetime.datetime = None
    ) -> None:
        """Set the start time.

        :param datetime.datetime start_time: The starting time to use for the computation, defaults to now.

        :raises pydantic.ValidationError: Raised when a parameter is invalid.

        :rtype: None
        """
        if start_time is None:
            start_time = datetime.datetime.now()

        self.start_time = start_time

    @validate_call
    def set_verbose(
            self,
            verbose: bool
    ) -> None:
        """Set the verbosity of the strings.

        :param bool verbose: If we should make strings verbosely or not.

        :raises pydantic.ValidationError: Raised when a parameter is invalid.

        :rtype: None
        """
        self.verbose = verbose

    @validate_call
    def set_percent_decimals(
            self,
            percent_decimals: NonNegativeInt
    ) -> None:
        """Set the number of decimal places to use in the percentage string.

        :param int percent_decimals: The number of decimal places to use in the percentage string.

        :rtype: None
        """
        self.percent_decimals = percent_decimals

    @validate_call
    def set_not_enough_data_string(
            self,
            not_enough_data_string: str
    ) -> None:
        """Set the string to return when there is not enough data for the desired computation.

        :param str not_enough_data_string: The string to return when there is not enough data for the desired computation.

        :rtype: None
        """
        self.not_enough_data_string = not_enough_data_string


@validate_call
def eta_calculator(
        items: Sequence[Any],
        start_time: datetime.datetime = None,
        verbose: bool = EtaDefaults.verbose,
        percent_decimals: NonNegativeInt = EtaDefaults.percent_decimals,
        not_enough_data_string: str = EtaDefaults.not_enough_data_string
) -> Iterator[tuple[Any, Eta]]:
    """A generator that iterates over the items in a sequence and returns the items in addition to an Eta object.

    :param Sequence[Any] items: The sequence to iterate over.
    :param datetime.datetime start_time: The starting time to use for the computation, defaults to now.
    :param bool verbose: If we should make strings verbosely or not.
    :param int percent_decimals: The number of decimal places to use in the percentage string.
    :param str not_enough_data_string: The string to return when there is not enough data for the desired computation.

    :return: Yield a tuple of the current item and the computed Eta object.
    :rtype: Iterator[tuple[Any, Eta]]
    """
    if start_time is None:
        start_time = datetime.datetime.now()

    calculator = EtaCalculator(
        total_items=len(items),
        start_time=start_time,
        verbose=verbose,
        percent_decimals=percent_decimals,
        not_enough_data_string=not_enough_data_string
    )

    for i, item in enumerate(items):
        yield item, calculator.get_eta(i)
