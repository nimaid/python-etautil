"""Provides tools to manipulate and format various time-based objects."""
import datetime
from dataclasses import dataclass
from pydantic import BaseModel, NonNegativeInt, NonNegativeFloat, PositiveInt, validate_call

from etautil.constants import TimeDefaults


class SplitTime(BaseModel):
    """Data class for holding split time values."""
    weeks: NonNegativeInt
    days: NonNegativeInt
    hours: NonNegativeInt
    minutes: NonNegativeInt
    seconds: NonNegativeInt
    milliseconds: NonNegativeInt | NonNegativeFloat


@validate_call
def split_seconds(seconds_in: NonNegativeInt | NonNegativeFloat) -> SplitTime:
    """Split seconds into parts ranging from weeks to milliseconds and return a SplitTime object with those values.

    :param int seconds_in: The total number of seconds to split up.

    :return: A SplitTime object with the split weeks, days, hours, minutes, seconds, and milliseconds.
    :rtype: SplitTime
    """
    weeks, remainder = divmod(seconds_in, (60 ** 2) * 24 * 7)
    days, remainder = divmod(remainder, (60 ** 2) * 24)
    hours, remainder = divmod(remainder, 60 ** 2)
    minutes, remainder = divmod(remainder, 60)
    seconds = int(remainder)
    milliseconds = (remainder % 1) * 1000

    return SplitTime(
        weeks=weeks,
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        milliseconds=milliseconds
    )


@validate_call
def day_of_month_suffix(day: PositiveInt) -> str:
    """Return the appropriate suffix for a specified day of the month.

    :param int day: The day of the month to get the suffix for.

    :return: A string that is either 'st', 'nd', 'rd', or 'th'.
    :rtype: str
    """
    if day % 100 in [11, 12, 13]:
        return "th"

    match day % 10:
        case 1:
            return "st"
        case 2:
            return "nd"
        case 3:
            return "rd"
        case _:
            return "th"


@validate_call
def day_of_month_string(day: PositiveInt) -> str:
    """Convert a numerical day of the month to a user-friendly string.

    :param int day: The day of the month to convert.

    :return: A string with the day of the month and an appropriate suffix ('st', 'nd', 'rd', or 'th').
    :rtype: str
    """
    return f"{day}{day_of_month_suffix(day)}"


@validate_call
def timezone_name(datetime_in: datetime.datetime) -> str:
    """Get the full timezone name from a datetime.datetime object.

    :param datetime.datetime datetime_in: The datetime.datetime object to get the timezone for.

    :return: A human-readable string with the full timezone name spelled out.
    :rtype: str
    """
    timezone = datetime_in.astimezone()

    return timezone.tzinfo.tzname(timezone)


@dataclass
class TimeString:
    """Data class with methods to format various datetime objects into human-readable strings."""
    @dataclass
    class TimeDelta:
        """Data class with methods to format datetime.timedelta objects and return human-readable strings."""
        @staticmethod
        @validate_call
        def short(timedelta_in: datetime.timedelta) -> str:
            """Return the datetime.timedelta object as a short human-readable string.

            :param datetime.timedelta timedelta_in: The timedelta to convert.

            :return: The datetime.timedelta object as a short human-readable string
            :rtype: str
            """
            ago_string = ""
            if timedelta_in < datetime.timedelta(0):
                timedelta_in = -timedelta_in
                ago_string += " ago"

            time_parts = split_seconds(timedelta_in.total_seconds())

            time_string = (f"{time_parts.hours}"
                           f":{time_parts.minutes:02}"
                           f":{time_parts.seconds:02}"
                           f"{ago_string}")

            if time_parts.days > 0:
                time_string = f"{time_parts.days}D {time_string}"

            if time_parts.weeks > 0:
                time_string = f"{time_parts.weeks}W {time_string}"

            return time_string

        @staticmethod
        @validate_call
        def long(timedelta_in: datetime.timedelta) -> str:
            """Return the datetime.timedelta object as a long human-readable string.

            :param datetime.timedelta timedelta_in: The timedelta to convert.

            :return: The datetime.timedelta object as a long human-readable string
            :rtype: str
            """
            ago_string = ""
            if timedelta_in < datetime.timedelta(0):
                timedelta_in = -timedelta_in
                ago_string += " ago"

            time_parts = split_seconds(timedelta_in.total_seconds())

            time_strings = []

            for value, name in (
                    (time_parts.weeks, "week"),
                    (time_parts.days, "day"),
                    (time_parts.hours, "hour"),
                    (time_parts.minutes, "minute"),
                    (time_parts.seconds, "second")
            ):
                if name == "second":
                    no_time_strings = len(time_strings) == 0
                else:
                    no_time_strings = False

                if value > 0 or no_time_strings:
                    time_strings.append(f"{value} {name}")
                    if value != 1:
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

    @dataclass
    class DateTime:
        """Data class with methods to format datetime.datetime objects and return human-readable strings."""
        @staticmethod
        @validate_call
        def short(datetime_in: datetime.datetime) -> str:
            """Return the datetime.datetime object as a short human-readable string.

            :param datetime.datetime datetime_in: The timedelta to convert.

            :return: The datetime.datetime object as a short human-readable string
            :rtype: str
            """
            now = datetime.datetime.now()

            format_string = "%#I:%M:%S %p"

            if datetime_in.day != now.day or datetime_in.year != now.year:
                format_string = f"%Y/%m/%d @ {format_string}"

            return datetime_in.strftime(format_string).strip()

        @staticmethod
        @validate_call
        def long(datetime_in: datetime.datetime) -> str:
            """Return the datetime.datetime object as a long human-readable string.

            :param datetime.datetime datetime_in: The timedelta to convert.

            :return: The datetime.datetime object as a long human-readable string
            :rtype: str
            """
            now = datetime.datetime.now()

            format_string = "%#I:%M:%S %p"

            if datetime_in.day != now.day or datetime_in.year != now.year:
                format_string = f"%A, %B {day_of_month_string(datetime_in.day)}, %Y at {format_string}"

            time_string = datetime_in.strftime(format_string).strip()
            time_string += f" {timezone_name(datetime_in)}"

            return time_string

    @staticmethod
    @validate_call
    def automatic(
            time_in: datetime.datetime | datetime.timedelta,
            verbose: bool
    ):
        """Automatically convert a datetime.datetime or datetime.timedelta object to a string and return it.

        :param datetime.datetime | datetime.timedelta time_in: The object to convert.
        :param verbose: If we should return the long or short version.

        :return: The input time in a human-readable format.
        :rtype: str
        """
        if isinstance(time_in, datetime.datetime):
            if verbose:
                return TimeString.DateTime.long(time_in)

            return TimeString.DateTime.short(time_in)

        if isinstance(time_in, datetime.timedelta):
            if verbose:
                return TimeString.TimeDelta.long(time_in)

            return TimeString.TimeDelta.short(time_in)

        return TimeDefaults.unknown_format_string  # Should never be called because pydantic validated the types
