from enum import Enum, unique


# unique decorator ensures that only one name is bound to any value
# if any duplicate values are found a ValueError is raised
@unique
class ForecastType(Enum):
    # using Enum class containing a set of unique properties to set constant values.
    # the values will be used to build the URL to make requests to the weather websites
    TODAY = 'today'
    FIVEDAYS = '5day'
    TENDAYS = '10day'
    WEEKEND = 'weekend'
