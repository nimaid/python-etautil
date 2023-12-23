"""Provides tools to format time-based objects into strings."""
import datetime

from .validate import Validate


class TimeString:
    """Container class with methods to process time-based objects and return human-readable strings."""
    @staticmethod
    def split_seconds(seconds_in):
        """Splits a seconds into days, hours, minutes, and seconds, and returns a dictionary with those values."""
        Validate.is_positive(seconds_in, "Seconds in")

        days, remainder = divmod(seconds_in, (60 ** 2) * 24)
        hours, remainder = divmod(remainder, 60 ** 2)
        minutes, seconds = divmod(remainder, 60)

        return {
            "d": days,
            "h": hours,
            "m": minutes,
            "s": seconds
        }

    class TimeDelta:
        @staticmethod
        def short(timedelta_in):
            Validate.is_type(timedelta_in, datetime.timedelta, "Input time")

            if timedelta_in < datetime.timedelta(0):
                timedelta_in = datetime.timedelta(0)

            time_parts = TimeString.split_seconds(round(timedelta_in.total_seconds()))

            time_string = f"{time_parts['s']:02}S"
            if time_parts["m"] > 0 or time_parts["h"] > 0 or time_parts["d"] > 0:
                time_string = f"{time_parts['m']:02}M:{time_string}"
            if time_parts["h"] > 0 or time_parts["d"] > 0:
                time_string = f"{time_parts['h']}H:{time_string}"
            if time_parts["d"] > 0:
                time_string = f"{time_parts['d']}D:{time_string}"

            return time_string

        @staticmethod
        def long(timedelta_in):
            Validate.is_type(timedelta_in, datetime.timedelta, "Input time")

            if timedelta_in < datetime.timedelta(0):
                timedelta_in = datetime.timedelta(0)

            time_parts = TimeString.split_seconds(round(timedelta_in.total_seconds()))

            time_strings = []
            if time_parts["d"] > 0:
                time_strings.append(f"{time_parts['d']} day")
                if time_parts["d"] != 1:
                    time_strings[-1] += "s"
            if time_parts["h"] > 0:
                time_strings.append(f"{time_parts['h']} hour")
                if time_parts["h"] != 1:
                    time_strings[-1] += "s"
            if time_parts["m"] > 0:
                time_strings.append(f"{time_parts['m']} minute")
                if time_parts["m"] != 1:
                    time_strings[-1] += "s"
            if len(time_strings) == 0 or time_parts["s"] > 0:
                time_strings.append(f"{time_parts['s']} second")
                if time_parts["s"] != 1:
                    time_strings[-1] += "s"

            if len(time_strings) == 1:
                time_string = time_strings[0]
            elif len(time_strings) == 2:
                time_string = f"{time_strings[0]} and {time_strings[1]}"
            else:
                time_string = ", ".join(time_strings[:-1])
                time_string += f", and {time_strings[-1]}"

            return time_string

    class DateTime:
        @staticmethod
        def short(datetime_in):
            Validate.is_type(datetime_in, datetime.datetime, "Input time")

            now = datetime.datetime.now()
            if datetime_in.day != now.day or datetime_in.year != now.year:
                return datetime_in.strftime("%Y/%m/%d @ %#I:%M:%S %p").strip()
            else:
                return datetime_in.strftime("%#I:%M:%S %p").strip()

        @staticmethod
        def long(datetime_in):
            Validate.is_type(datetime_in, datetime.datetime, "Input time")

            now = datetime.datetime.now()
            if datetime_in.day != now.day or datetime_in.year != now.year:
                return datetime_in.strftime("%A, %B %#d, %Y @ %#I:%M:%S %p %Z").strip()
            else:
                return datetime_in.strftime("%#I:%M:%S %p %Z").strip()
