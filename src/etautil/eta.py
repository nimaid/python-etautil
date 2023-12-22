import datetime

from .timestring import TimeString


class Eta:
    def __init__(self, total_items, start_time=None, verbose=False):
        if start_time is None:
            self.start_time = datetime.datetime.now()
        else:
            self.start_time = start_time

        self.total_items = total_items
        self.verbose = verbose

    def set_total_items(self, total_items):
        self.total_items = total_items

    def get_total_items(self):
        return self.total_items

    def set_verbose(self, verbose):
        self.verbose = verbose

    def get_verbose(self):
        return self.verbose

    def get_time_taken(self, current_time=None):
        if current_time is None:
            current_time = datetime.datetime.now()

        return current_time - self.start_time

    def get_time_taken_string(self, current_time=None):
        if current_time is None:
            current_time = datetime.datetime.now()

        time_taken = self.get_time_taken(current_time)

        if self.verbose:
            return TimeString.TimeDelta.long(time_taken)
        else:
            return TimeString.TimeDelta.short(time_taken)

    def get_eta_difference(self, current_item_index):
        if current_item_index < 1:
            raise ValueError("Unable to compute ETA for the first item (infinite time)")

        if current_item_index > self.total_items:
            raise IndexError("Item index is larger than the total items")

        current_time = datetime.datetime.now()
        time_taken = self.get_time_taken(current_time)
        percent_done = self.get_percentage(current_item_index)

        progress_scale = (1 - percent_done) / percent_done
        eta_diff = time_taken * progress_scale
        eta = current_time + eta_diff

        return eta, eta_diff

    def get_eta(self, current_item_index):
        return self.get_eta_difference(current_item_index)[0]

    def get_eta_string(self, current_item_index):
        eta = self.get_eta(current_item_index)

        if self.verbose:
            return TimeString.DateTime.long(eta)
        else:
            return TimeString.DateTime.short(eta)

    def get_difference(self, current_item_index):
        return self.get_eta_difference(current_item_index)[1]

    def get_difference_string(self, current_item_index):
        difference = self.get_difference(current_item_index)

        if self.verbose:
            return TimeString.TimeDelta.long(difference)
        else:
            return TimeString.TimeDelta.short(difference)

    def get_start_time(self):
        return self.start_time

    def get_start_time_string(self):
        if self.verbose:
            return TimeString.DateTime.long(self.start_time)
        else:
            return TimeString.DateTime.short(self.start_time)

    def get_percentage(self, current_item_index):
        if current_item_index < 0:
            raise ValueError("Item index cannot be less than 0")

        if current_item_index > self.total_items:
            raise IndexError("Item index is larger than the total items")

        return current_item_index / (self.total_items - 1)

    def get_percentage_string(self, current_item_index, decimals=2):
        percentage = self.get_percentage(current_item_index) * 100
        format_string = f"{{:.{decimals}f}}%"
        percent_string = format_string.format(percentage)

        if self.verbose:
            percent_string += f" ({current_item_index + 1}/{self.total_items})"

        return percent_string

    def get_progress_string(self, current_item_index, sep=" | ", percent_decimals=2):
        percent_string = self.get_percentage_string(current_item_index, decimals=percent_decimals)

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
