from enum import Enum


class BaseEnum(Enum):

    def _generate_next_value_(name, start, count, last_values):
        # method is an Enum method which has been overridden
        # every Enum class that inherits from BaseEnum that has its values set to auto()
        # will get the same value as the Enum class variable name
        return name
