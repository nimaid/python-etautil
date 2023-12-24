import pendulum
from pydantic import Field, validate_call
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
            total_items: Annotated[int, Field(gt=2)],
            start_time: pendulum.DateTime = None,
            verbose: bool = False,
            percent_decimals: Annotated[int, Field(gt=0)] = 2
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

    @validate_call
    def set_total_items(
            self,
            total_items: Annotated[int, Field(gt=2)]
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

    def get_start_time_string(self) -> str:
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
            percent_decimals: int
    ) -> None:
        self.percent_decimals = percent_decimals

    def get_percent_decimals(self) -> int:
        return self.percent_decimals

    @validate_call
    def get_time_taken(
            self,
            current_time: pendulum.DateTime = None
    ) -> pendulum.Duration:
        if current_time is None:
            current_time = pendulum.now()

        return current_time - self.start_time

    @validate_call
    def get_time_taken_string(
            self,
            current_time: pendulum.DateTime = None
    ) -> str:
        if current_time is None:
            current_time = pendulum.now()

        return self.get_time_taken(current_time).in_words()

    @validate_call
    def get_difference(
            self,
            current_item_index,
            current_time=None
    ):
        if current_time is None:
            current_time = pendulum.now()

        time_taken = self.get_time_taken(current_time)
        percent_done = self.get_percentage(current_item_index)

        progress_scale = (1 - percent_done) / percent_done
        return time_taken * progress_scale

    def get_difference_string(self, current_item_index):
        return self.get_difference(current_item_index).in_words()

    def get_eta(self, current_item_index, current_time=None):
        now = pendulum.now()

        class Params(NoneDefaultModel):
            current_time: typing.Optional[pendulum.DateTime] = now

            class Config:
                arbitrary_types_allowed = True

        params = Params(
            current_time=current_time
        )

        assert params.current_time is not None

        eta_diff = self.get_difference(
            current_item_index=current_item_index,
            current_time=params.current_time
        )
        eta = params.current_time + eta_diff

        return eta

    def get_eta_string(self, current_item_index):
        return self.get_eta(current_item_index).format(self.datetime_format)

    def get_percentage(self, current_item_index):
        class Params(BaseModel):
            current_item_index: PositiveInt = Field(None, ge=1, le=(self.total_items - 1))

        params = Params(
            current_item_index=current_item_index,
        )

        return params.current_item_index / (self.total_items - 1)

    def get_percentage_string(self, current_item_index):
        class Params(BaseModel):
            current_item_index: PositiveInt = Field(None, ge=1, le=(self.total_items - 1))

        params = Params(
            current_item_index=current_item_index,
        )

        percentage = self.get_percentage(params.current_item_index) * 100
        format_string = f"{{:.{self.percent_decimals}f}}%"
        percent_string = format_string.format(percentage)

        if self.verbose:
            percent_string += f" ({params.current_item_index + 1}/{self.total_items})"

        return percent_string

    def get_progress_string(self, current_item_index, sep=" | "):
        class Params(BaseModel):
            current_item_index: PositiveInt = Field(None, ge=1, le=(self.total_items - 1))
            sep: str

        params = Params(
            current_item_index=current_item_index,
            sep=sep
        )

        percent_string = self.get_percentage_string(params.current_item_index)

        if params.current_item_index <= 0:
            return percent_string

        difference_string = self.get_difference_string(params.current_item_index)
        eta_string = self.get_eta_string(params.current_item_index)
        if self.verbose:
            return params.sep.join([percent_string, f"Time remaining: {difference_string}", f"ETA: {eta_string}"])
        else:
            return params.sep.join([percent_string, difference_string, eta_string])
