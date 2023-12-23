class Validate:
    @staticmethod
    def type(value, value_type, value_name):
        if not isinstance(value, value_type):
            raise TypeError(f"{value_name} must be a "
                            f"{value_type.__qualname__} object (got a "
                            f"{type(value).__qualname__} object)")

    @staticmethod
    def positive(value, value_name):
        if value < 0:
            raise ValueError(f"{value_name} must not be negative")
