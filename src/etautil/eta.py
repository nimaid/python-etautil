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

    def set_verbose(self, verbose):
        self.verbose = verbose

    def set_total_items(self, total_items):
        self.total_items = total_items

    def get_time_taken(self, current_time=None):
        if current_time is None:
            current_time = datetime.datetime.now()

        return current_time - self.start_time

    def get_eta(self, current_item_index):
        if current_item_index < 1:
            raise ValueError("Unable to compute ETA for the first item (infinite time)")

        if current_item_index > self.total_items:
            raise IndexError("Item index is larger than the total items")

        current_time = datetime.datetime.now()
        time_taken = self.get_time_taken(current_time)
        percent_done = current_item_index / (self.total_items - 1)
        progress_scale = (1 - percent_done) / percent_done
        eta_diff = time_taken * progress_scale
        eta = current_time + eta_diff

        return {
            "eta": eta,
            "difference": eta_diff
        }

    def get_start_time(self):
        return self.start_time

    def get_time_taken_string(self, current_time=None):
        if current_time is None:
            current_time = datetime.datetime.now()

        time_taken = self.get_time_taken(current_time)

        if self.verbose:
            return TimeString.TimeDelta.long(time_taken)
        else:
            return TimeString.TimeDelta.short(time_taken)

    def get_start_time_string(self):
        if self.verbose:
            return TimeString.DateTime.long(self.start_time)
        else:
            return TimeString.DateTime.short(self.start_time)

    def get_time_remaining_string(self, current_item_index):
        eta = self.get_eta(current_item_index)

        if self.verbose:
            difference_string = TimeString.TimeDelta.long(eta["difference"])
            eta_string = TimeString.DateTime.long(eta["eta"])
        else:
            difference_string = TimeString.TimeDelta.short(eta["difference"])
            eta_string = TimeString.DateTime.short(eta["eta"])

        return f"Time remaining: {difference_string} | ETA: {eta_string}"

    def get_eta_string(self, current_item_index):
        eta = self.get_eta(current_item_index)

        if self.verbose:
            return TimeString.DateTime.long(eta["eta"])
        else:
            return TimeString.DateTime.short(eta["eta"])

    def get_difference_string(self, current_item_index):
        eta = self.get_eta(current_item_index)

        if self.verbose:
            return TimeString.TimeDelta.long(eta["difference"])
        else:
            return TimeString.TimeDelta.short(eta["difference"])
