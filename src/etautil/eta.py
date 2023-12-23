import pendulum

from .validate import Validate


class Eta:
    def __init__(self, total_items, start_time=None, verbose=False, percent_decimals=2):
        self.total_items = None
        self.set_total_items(total_items)

        self.start_time = None
        self.set_start_time(start_time)

        self.verbose = None
        self.datetime_format = None
        self.set_verbose(verbose)

        self.percent_decimals = None
        self.set_percent_decimals(percent_decimals)

    @staticmethod
    def __validate_total_items(total_items):
        Validate.is_type(total_items, int, "Total items")

        if total_items < 2:
            raise ValueError("Total items must be at least 2 to compute an ETA")

    @staticmethod
    def __validate_percent_decimals(percent_decimals):
        Validate.is_type(percent_decimals, int, "Percent decimals")
        Validate.is_positive(percent_decimals, "Percent decimals")

    def __validate_index(self, index):
        Validate.is_type(index, int, "Item index")
        Validate.is_positive(index, "Item index")

        if index > self.total_items - 1:
            raise IndexError("Item index is larger than the total items - 1")

    def __validate_index_eta(self, index):
        self.__validate_index(index)

        if index < 1:
            raise ValueError("Unable to compute ETA for the first item (infinite time)")

    def set_total_items(self, total_items):
        self.__validate_total_items(total_items)

        self.total_items = total_items

    def get_total_items(self):
        return self.total_items

    def set_start_time(self, start_time=None):
        if start_time is None:
            self.start_time = pendulum.now()
        else:
            Validate.is_type(start_time, pendulum.DateTime, "Start time")

            self.start_time = start_time

    def get_start_time(self):
        return self.start_time

    def get_start_time_string(self):
        return self.start_time.format(self.datetime_format)

    def set_verbose(self, verbose):
        if not isinstance(verbose, bool):
            raise ValueError("Verbose setting must be a boolean value")

        self.verbose = verbose

        if self.verbose:
            self.datetime_format = "dddd, MMMM Do, YYYY @ h:mm:ss A Z"
        else:
            self.datetime_format = "YYYY/MM/DD @ h:mm:ss A"

    def get_verbose(self):
        return self.verbose

    def set_percent_decimals(self, percent_decimals):
        self.__validate_percent_decimals(percent_decimals)

        self.percent_decimals = percent_decimals

    def get_percent_decimals(self):
        return self.percent_decimals

    def get_time_taken(self, current_time=None):
        if current_time is None:
            current_time = pendulum.now()

        Validate.is_type(current_time, pendulum.DateTime, "Current time")

        return current_time - self.start_time

    def get_time_taken_string(self, current_time=None):
        if current_time is None:
            current_time = pendulum.now()

        Validate.is_type(current_time, pendulum.DateTime, "Current time")

        time_taken = self.get_time_taken(current_time)

        return time_taken.in_words()

    def get_eta_difference(self, current_item_index):
        self.__validate_index_eta(current_item_index)

        current_time = pendulum.now()
        time_taken = self.get_time_taken(current_time)
        percent_done = self.get_percentage(current_item_index)

        progress_scale = (1 - percent_done) / percent_done
        eta_diff = time_taken * progress_scale
        eta = current_time + eta_diff

        return eta, eta_diff

    def get_eta(self, current_item_index):
        self.__validate_index_eta(current_item_index)

        return self.get_eta_difference(current_item_index)[0]

    def get_eta_string(self, current_item_index):
        self.__validate_index_eta(current_item_index)

        eta = self.get_eta(current_item_index)

        return eta.format(self.datetime_format)

    def get_difference(self, current_item_index):
        self.__validate_index_eta(current_item_index)

        return self.get_eta_difference(current_item_index)[1]

    def get_difference_string(self, current_item_index):
        self.__validate_index_eta(current_item_index)

        difference = self.get_difference(current_item_index)

        return difference.in_words()

    def get_percentage(self, current_item_index):
        self.__validate_index(current_item_index)

        return current_item_index / (self.total_items - 1)

    def get_percentage_string(self, current_item_index):
        Validate.is_type(current_item_index, int, "Item index")

        percentage = self.get_percentage(current_item_index) * 100
        format_string = f"{{:.{self.percent_decimals}f}}%"
        percent_string = format_string.format(percentage)

        if self.verbose:
            percent_string += f" ({current_item_index + 1}/{self.total_items})"

        return percent_string

    def get_progress_string(self, current_item_index, sep=" | "):
        self.__validate_index(current_item_index)
        Validate.is_type(sep, str, "Seperator")

        percent_string = self.get_percentage_string(current_item_index)

        if current_item_index <= 0:
            return percent_string

        eta, difference = self.get_eta_difference(current_item_index)

        difference_string = difference.in_words()
        eta_string = eta.format(self.datetime_format)
        if self.verbose:
            return sep.join((percent_string, f"Time remaining: {difference_string}", f"ETA: {eta_string}"))
        else:
            return sep.join((percent_string, difference_string, eta_string))
