import pendulum
from pydantic import NonNegativeInt, Field, validate_call
from typing_extensions import Annotated


class Eta:
    """A simple abstraction for computing and formatting time estimates.

    :param int total_items: The total number of items to process, used in computations.
    :param pendulum.DateTime start_time: The starting time used in all calculations, defaults to the current time.
    :param bool verbose: If we should make strings verbosely or not.
    :param int percent_decimals: The number of decimal places to use in the percentage string.
    :raises pydantic.ValidationError: Raised when a parameter is invalid.
    :return: A new Eta abstraction object.
    :rtype: Eta
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
        #: The format string to use for DateTime, based on self.verbose.
        self.datetime_format = None
        self.set_verbose(verbose)

        self.percent_decimals = None
        self.set_percent_decimals(percent_decimals)

    def _validate_item_index(
            self,
            item_index: NonNegativeInt
    ) -> None:
        """Validate that an index is not larger than the total items and raise an IndexError otherwise.

        :param int item_index: The index to test.
        :raises IndexError: Raised when the index is too large.
        :rtype: None
        """
        if item_index > self.total_items - 1:
            raise IndexError(f"Item index should be less than {self.total_items - 1} (the total items - 1)")

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

    def get_total_items(self) -> int:
        """Get the total number of items to process.

        :return: The total number of items to process, used in computations.
        :rtype: int
        """
        return self.total_items

    @validate_call(config={'arbitrary_types_allowed': True})
    def set_start_time(
            self,
            start_time: pendulum.DateTime = None
    ) -> None:
        if start_time is None:
            start_time = pendulum.now()

        self.start_time = start_time

    def get_start_time(self) -> pendulum.DateTime:
        return self.start_time

    def start_time_string(self) -> str:
        return self.start_time.format(self.datetime_format)

    @validate_call
    def set_verbose(
            self,
            verbose: bool
    ) -> None:
        self.verbose = verbose

        if self.verbose:
            self.datetime_format = "dddd, MMMM Do, YYYY @ h:mm:ss A Z"
        else:
            self.datetime_format = "YYYY/MM/DD @ h:mm:ss A"

    def get_verbose(self) -> bool:
        return self.verbose

    @validate_call
    def set_percent_decimals(
            self,
            percent_decimals: NonNegativeInt
    ) -> None:
        self.percent_decimals = percent_decimals

    def get_percent_decimals(self) -> int:
        return self.percent_decimals

    @validate_call(config={'arbitrary_types_allowed': True})
    def time_taken(
            self,
            current_time: pendulum.DateTime = None
    ) -> pendulum.Duration:
        if current_time is None:
            current_time = pendulum.now()

        return current_time - self.start_time

    @validate_call(config={'arbitrary_types_allowed': True})
    def time_taken_string(
            self,
            current_time: pendulum.DateTime = None
    ) -> str:
        if current_time is None:
            current_time = pendulum.now()

        return self.time_taken(current_time).in_words()

    @validate_call(config={'arbitrary_types_allowed': True})
    def time_remaining(
            self,
            current_item_index: NonNegativeInt,
            current_time: pendulum.DateTime = None
    ) -> pendulum.Duration:
        self._validate_item_index(current_item_index)

        if current_time is None:
            current_time = pendulum.now()

        time_taken = self.time_taken(current_time)
        percent_done = self.percentage(current_item_index)

        progress_scale = (1 - percent_done) / percent_done
        return time_taken * progress_scale

    @validate_call(config={'arbitrary_types_allowed': True})
    def time_remaining_string(
            self,
            current_item_index: NonNegativeInt,
            current_time: pendulum.DateTime = None
    ) -> str:
        self._validate_item_index(current_item_index)

        if current_time is None:
            current_time = pendulum.now()

        return self.time_remaining(
            current_item_index=current_item_index,
            current_time=current_time
        ).in_words()

    @validate_call(config={'arbitrary_types_allowed': True})
    def eta(
            self,
            current_item_index: NonNegativeInt,
            current_time: pendulum.DateTime = None
    ) -> pendulum.DateTime:
        self._validate_item_index(current_item_index)

        if current_time is None:
            current_time = pendulum.now()

        eta_diff = self.time_remaining(
            current_item_index=current_item_index,
            current_time=current_time
        )
        eta = current_time + eta_diff

        return eta

    @validate_call(config={'arbitrary_types_allowed': True})
    def eta_string(
            self,
            current_item_index: NonNegativeInt,
            current_time: pendulum.DateTime = None
    ) -> str:
        self._validate_item_index(current_item_index)

        if current_time is None:
            current_time = pendulum.now()

        return self.eta(
            current_item_index=current_item_index,
            current_time=current_time
        ).format(self.datetime_format)

    @validate_call
    def percentage(
            self,
            current_item_index: NonNegativeInt
    ) -> float:
        self._validate_item_index(current_item_index)

        return current_item_index / (self.total_items - 1)

    @validate_call
    def percentage_string(
            self,
            current_item_index: NonNegativeInt
    ) -> str:
        self._validate_item_index(current_item_index)

        percentage = self.percentage(current_item_index) * 100
        format_string = f"{{:.{self.percent_decimals}f}}%"
        percent_string = format_string.format(percentage)

        if self.verbose:
            percent_string += f" ({current_item_index + 1}/{self.total_items})"

        return percent_string

    @validate_call
    def progress_string(
            self,
            current_item_index: NonNegativeInt,
            sep: str = " | "
    ) -> str:
        self._validate_item_index(current_item_index)

        current_time = pendulum.now()

        percent_string = self.percentage_string(current_item_index)

        if current_item_index <= 0:
            return percent_string

        difference_string = self.time_remaining_string(
            current_item_index=current_item_index,
            current_time=current_time
        )
        eta_string = self.eta_string(
            current_item_index=current_item_index,
            current_time=current_time
        )

        if self.verbose:
            difference_string = f"Time remaining: {difference_string}"
            eta_string = f"ETA: {eta_string}"

        return sep.join([percent_string, difference_string, eta_string])
