import datetime


class TimeString:
    @staticmethod
    def split_seconds(seconds_in):
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
        def short(time_in):
            if time_in < datetime.timedelta(0):
                time_in = datetime.timedelta(0)

            time_parts = TimeString.split_seconds(round(time_in.total_seconds()))

            time_string = f"{time_parts['s']:02}S"
            if time_parts["m"] > 0 or time_parts["h"] > 0 or time_parts["d"] > 0:
                time_string = f"{time_parts['m']:02}M:{time_string}"
            if time_parts["h"] > 0 or time_parts["d"] > 0:
                time_string = f"{time_parts['h']}H:{time_string}"
            if time_parts["d"] > 0:
                time_string = f"{time_parts['d']}D:{time_string}"

            return time_string

        @staticmethod
        def long(time_in):
            if time_in < datetime.timedelta(0):
                time_in = datetime.timedelta(0)

            time_parts = TimeString.split_seconds(round(time_in.total_seconds()))

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
        def short(time_in):
            now = datetime.datetime.now()
            if time_in.day != now.day or time_in.year != now.year:
                return time_in.strftime("%Y/%m/%d @ %#I:%M:%S %p").strip()
            else:
                return time_in.strftime("%#I:%M:%S %p").strip()

        @staticmethod
        def long(time_in):
            now = datetime.datetime.now()
            if time_in.day != now.day or time_in.year != now.year:
                return time_in.strftime("%A, %B %#d, %Y @ %#I:%M:%S %p %Z").strip()
            else:
                return time_in.strftime("%#I:%M:%S %p %Z").strip()
