import datetime

from .timestring import TimeString


class Eta:
    def __init__(self, total_items, start_time=None, verbose=False, percent_decimals=2):
        self.total_items = None
        self.set_total_items(total_items)

        self.start_time = None
        self.set_start_time(start_time)

        self.verbose = None
        self.set_verbose(verbose)

        self.percent_decimals = None
        self.set_percent_decimals(percent_decimals)

    @staticmethod
    def _validate_int(int_in, property_name):
        if not isinstance(int_in, int):
            raise ValueError(f"{property_name} must be an int")

    @staticmethod
    def _validate_bool(bool_in, property_name):
        if not isinstance(bool_in, int):
            raise ValueError(f"{property_name} must be a bool")

    @staticmethod
    def _validate_string(string_in, property_name):
        if not isinstance(string_in, str):
            raise ValueError(f"{property_name} must be a string")

    @staticmethod
    def _validate_datetime(date_time, property_name):
        if not isinstance(date_time, datetime.datetime):
            raise ValueError(f"{property_name} must be a datetime object")

    def _validate_index(self, index):
        self._validate_int(index, "Item index")

        if index <= 0:
            raise ValueError("Item index cannot be negative")

        if index > self.total_items - 1:
            raise IndexError("Item index is larger than the total items - 1")

    def _validate_index_eta(self, index):
        self._validate_index(index)

        if index < 1:
            raise ValueError("Unable to compute ETA for the first item (infinite time)")

    def _validate_total_items(self, total_items):
        self._validate_int(total_items, "Total items")

        if total_items < 2:
            raise ValueError("Total items must be at least 2 to compute an ETA")

    def _validate_percent_decimals(self, percent_decimals):
        self._validate_bool(percent_decimals, "Percent decimals")

        if percent_decimals < 0:
            raise ValueError("Percent decimals must not be negative")

    def set_total_items(self, total_items):
        self._validate_total_items(total_items)

        self.total_items = total_items

    def get_total_items(self):
        return self.total_items

    def set_start_time(self, start_time=None):
        if start_time is None:
            self.start_time = datetime.datetime.now()
        else:
            self._validate_datetime(start_time, "Start time")

            self.start_time = start_time

    def get_start_time(self):
        return self.start_time

    def get_start_time_string(self):
        if self.verbose:
            return TimeString.DateTime.long(self.start_time)
        else:
            return TimeString.DateTime.short(self.start_time)

    def set_verbose(self, verbose):
        if not isinstance(verbose, bool):
            raise ValueError("Verbose setting must be a boolean value")

        self.verbose = verbose

    def get_verbose(self):
        return self.verbose

    def set_percent_decimals(self, percent_decimals):
        self._validate_percent_decimals(percent_decimals)

        self.percent_decimals = percent_decimals

    def get_percent_decimals(self):
        return self.percent_decimals

    def get_time_taken(self, current_time=None):
        if current_time is None:
            current_time = datetime.datetime.now()

        self._validate_datetime(current_time, "Current time")

        return current_time - self.start_time

    def get_time_taken_string(self, current_time=None):
        if current_time is None:
            current_time = datetime.datetime.now()

        self._validate_datetime(current_time, "Current time")

        time_taken = self.get_time_taken(current_time)

        if self.verbose:
            return TimeString.TimeDelta.long(time_taken)
        else:
            return TimeString.TimeDelta.short(time_taken)

    def get_eta_difference(self, current_item_index):
        self._validate_index_eta(current_item_index)

        current_time = datetime.datetime.now()
        time_taken = self.get_time_taken(current_time)
        percent_done = self.get_percentage(current_item_index)

        progress_scale = (1 - percent_done) / percent_done
        eta_diff = time_taken * progress_scale
        eta = current_time + eta_diff

        return eta, eta_diff

    def get_eta(self, current_item_index):
        self._validate_index_eta(current_item_index)

        return self.get_eta_difference(current_item_index)[0]

    def get_eta_string(self, current_item_index):
        self._validate_index_eta(current_item_index)

        eta = self.get_eta(current_item_index)

        if self.verbose:
            return TimeString.DateTime.long(eta)
        else:
            return TimeString.DateTime.short(eta)

    def get_difference(self, current_item_index):
        self._validate_index_eta(current_item_index)

        return self.get_eta_difference(current_item_index)[1]

    def get_difference_string(self, current_item_index):
        self._validate_index_eta(current_item_index)

        difference = self.get_difference(current_item_index)

        if self.verbose:
            return TimeString.TimeDelta.long(difference)
        else:
            return TimeString.TimeDelta.short(difference)

    def get_percentage(self, current_item_index):
        self._validate_index_eta(current_item_index)

        return current_item_index / (self.total_items - 1)

    def get_percentage_string(self, current_item_index):
        self._validate_int(current_item_index, "Item index")

        if current_item_index <= 0:
            raise ValueError("Item index cannot be negative")

        percentage = self.get_percentage(current_item_index) * 100
        format_string = f"{{:.{self.percent_decimals}f}}%"
        percent_string = format_string.format(percentage)

        if self.verbose:
            percent_string += f" ({current_item_index + 1}/{self.total_items})"

        return percent_string

    def get_progress_string(self, current_item_index, sep=" | "):
        self._validate_index(current_item_index)
        self._validate_string(sep, "Seperator")

        percent_string = self.get_percentage_string(current_item_index)

        if current_item_index <= 0:
            return percent_string

        eta, difference = self.get_eta_difference(current_item_index)

        if self.verbose:
            difference_string = TimeString.TimeDelta.long(difference)
            eta_string = TimeString.DateTime.long(eta)
        else:
            difference_string = TimeString.TimeDelta.short(difference)
            eta_string = TimeString.DateTime.short(eta)

        return sep.join((percent_string, f"Time remaining: {difference_string}", f"ETA: {eta_string}"))
