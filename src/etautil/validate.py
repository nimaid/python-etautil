"""Provides tools to validate parameters of functions."""
import numbers


class Validate:
    """Container class with methods to validate common conditions about a value and raise an error if relevant."""
    @staticmethod
    def is_str(value, value_name: str) -> None:
        """Validate if a value is a string object.

        :param value: The value to be tested.
        :param str value_name: The name of the value, used in the error message.
        :raises TypeError: Raised when the value name isn't a string object.
        :raises TypeError: Raised when the value isn't a string object.
        :return: Nothing.
        :rtype: None
        """
        if not isinstance(value_name, str):
            raise TypeError(f"Value name must be a str object (got a {value_name.__qualname__} object)")

        if not isinstance(value, str):
            raise TypeError(f"{value_name} must be a str object (got a {value.__qualname__} object)")

    @staticmethod
    def not_empty(value, value_name: str) -> None:
        """ Validate if a value is not empty (None, "", [], False).

        :param value: The value to be tested.
        :param str value_name: The name of the value, used in the error message.
        :raises ValueError: Raised when the value is empty.
        :return: Nothing.
        :rtype: None
        """
        Validate.is_str(value_name, "Value name")

        if not value:
            raise ValueError(f"{value_name} name must not be blank")

    @staticmethod
    def value_name(value_name: str) -> None:
        """ Validate if a value name is valid.

        :param str value_name: The value name to be tested.
        :return: Nothing.
        :rtype: None
        """
        Validate.is_str(value_name, "Value name")
        Validate.not_empty(value_name, "Value name")

    @staticmethod
    def is_type(value, value_type: type, value_name: str) -> None:
        """Validate if a value matches a specified type.

        :param value: The value to be tested.
        :param type value_type: The type to test for.
        :param str value_name: The name of the value, used in the error message.
        :raises TypeError: Raised when the value type isn't a type object.
        :raises TypeError: Raised when the value name isn't a str object.
        :raises TypeError: Raised when the type(value) does not match the value type.
        :return: Nothing.
        :rtype: None
        """
        Validate.value_name(value_name)

        if not isinstance(value_type, type):
            raise TypeError(f"Value type must be a type object (got a {type(value).__qualname__} object)")

        if not isinstance(value_name, str):
            raise TypeError(f"Value name must be a str object (got a {type(value_name).__qualname__} object)")

        if not isinstance(value, value_type):
            raise TypeError(f"{value_name} must be a "
                            f"{value_type.__qualname__} object (got a "
                            f"{type(value).__qualname__} object)")

    @staticmethod
    def is_number(value, value_name: str) -> None:
        """Validate if a value is a real number.

        :param value: The value to be tested.
        :param value_name: The name of the value, used in the error message.
        :type value_name: str
        :raises TypeError: Raised when the value is not a real number.
        :return: Nothing.
        :rtype: None
        """
        Validate.value_name(value_name)

        if not isinstance(value, numbers.Real):
            raise ValueError(f"{value_name} must be a number, not a {type(value).__qualname__} object")

    @staticmethod
    def is_positive(value, value_name: str) -> None:
        """Validate if a value is not negative.

        :param value: The value to be tested.
        :param str value_name: The name of the value, used in the error message.
        :raises ValueError: Raised when the value is less than zero.
        :return: Nothing.
        :rtype: None
        """
        Validate.value_name(value_name)
        Validate.is_number(value, value_name)

        if value < 0:
            raise ValueError(f"{value_name} must not be negative")
