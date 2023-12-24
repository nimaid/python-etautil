"""Provides tools to format various datetime objects into human-readable strings."""
import datetime
from pydantic import NonNegativeInt, NonNegativeFloat, validate_call
from typing import Union


@validate_call
def split_seconds(seconds_in: Union[NonNegativeInt, NonNegativeFloat]) -> dict[str, Union[int, float]]:
    """Split seconds into days, hours, minutes, and seconds, and return a dictionary with those values.

    :param int seconds_in: The total number of seconds to split up.
    :return: A dictionary with the split weeks ['w'], days ['d'], hours ['h'], minutes ['m'], and seconds ['s'].
    :rtype: dict[str, Union[int, float]]
    """
    weeks, remainder = divmod(seconds_in, (60 ** 2) * 24 * 7)
    days, remainder = divmod(remainder, (60 ** 2) * 24)
    hours, remainder = divmod(remainder, 60 ** 2)
    minutes, seconds = divmod(remainder, 60)

    return {
        "w": round(weeks),
        "d": round(days),
        "h": round(hours),
        "m": round(minutes),
        "s": seconds
    }


class TimeString:
    """Container class with methods to process time-based objects and return human-readable strings."""
    class TimeDelta:
        """Container class with methods to process datetime.timedelta objects and return human-readable strings."""
        @staticmethod
        @validate_call
        def short(timedelta_in: datetime.timedelta) -> str:
            ago_string = ""
            if timedelta_in < datetime.timedelta(0):
                timedelta_in = -timedelta_in
                ago_string += " ago"

            time_parts = split_seconds(round(timedelta_in.total_seconds()))

            time_string = (f"{time_parts['h']}"
                           f":{time_parts['m']:02}"
                           f":{time_parts['s']:02}"
                           f"{ago_string}")

            if time_parts['d'] > 0:
                time_string = f"{time_parts['d']}D {time_string}"

            if time_parts['w'] > 0:
                time_string = f"{time_parts['w']}W {time_string}"

            return time_string

        @staticmethod
        @validate_call
        def long(timedelta_in: datetime.timedelta) -> str:
            ago_string = ""
            if timedelta_in < datetime.timedelta(0):
                timedelta_in = -timedelta_in
                ago_string += " ago"

            time_parts = split_seconds(round(timedelta_in.total_seconds()))

            time_strings = []

            for key, name in (("w", "week"), ("d", "day"), ("h", "hour"), ("m", "minute"), ("s", "second")):
                if key == "s":
                    no_time_strings = len(time_strings) == 0
                else:
                    no_time_strings = False

                if time_parts[key] > 0 or no_time_strings:
                    time_strings.append(f"{time_parts[key]} {name}")
                    if time_parts[key] != 1:
                        time_strings[-1] += "s"

            if len(time_strings) == 1:
                time_string = f"{time_strings[0]}{ago_string}"
            elif len(time_strings) == 2:
                time_string = f"{time_strings[0]} and {time_strings[1]}{ago_string}"
            else:
                time_string = ", ".join(time_strings[:-1])
                time_string += f", and {time_strings[-1]}"
                time_string += ago_string

            return time_string

    class DateTime:
        """Container class with methods to process datetime.datetime objects and return human-readable strings."""
        @staticmethod
        @validate_call
        def short(datetime_in: datetime.datetime) -> str:
            now = datetime.datetime.now()

            format_string = "%#I:%M:%S %p"

            if datetime_in.day != now.day or datetime_in.year != now.year:
                format_string = f"%Y/%m/%d @ {format_string}"

            return datetime_in.strftime(format_string).strip()

        @staticmethod
        @validate_call
        def long(datetime_in: datetime.datetime) -> str:
            now = datetime.datetime.now()

            format_string = "%#I:%M:%S %p"

            if datetime_in.day != now.day or datetime_in.year != now.year:
                match datetime_in.day % 10:
                    case 1:
                        day_suffix = "st"
                    case 2:
                        day_suffix = "nd"
                    case 3:
                        day_suffix = "rd"
                    case _:
                        day_suffix = "th"
                format_string = f"%A, %B %#d{day_suffix}, %Y @ {format_string}"

            time_string = datetime_in.strftime(format_string).strip()
            timezone = datetime_in.astimezone()
            time_string += f" {timezone.tzinfo.tzname(timezone)}"

            return time_string
