from .base_enum import BaseEnum
from enum import auto, unique


@unique
class Unit(BaseEnum):
    """Unit Enum class inherits from BaseEnum class in base_enum.py. Therefore since it's values are auto,
    the name of the enum becomes the value of enum"""
    CELSIUS = auto()
    FAHRENHEIT = auto()
