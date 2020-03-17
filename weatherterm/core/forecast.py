from .forecast_type import ForecastType
from datetime import date


class Forecast:
    """A Class to represent the properties for the forecast data going to be parsed"""

    def __init__(
            self,
            current_temp,
            humidity,
            wind,
            high_temp=None,
            low_temp=None,
            description='',
            forecast_date=None,
            forecast_type=ForecastType.TODAY
    ):
        self._current_temp = current_temp
        self._humidity = humidity
        self._wind = wind
        self._high_temp = high_temp
        self._low_temp = low_temp
        self._description = description
        self._forecast_date = forecast_date
        self._forecast_type = forecast_type

        if forecast_date is None:
            self._forecast_date = date.today()  # datetime.date.today() returns current local date eg (2019, 4, 3)
        else:
            self._forecast_date = forecast_date

    # using getters and setters to return and set attributes
    @property
    def current_temp(self):
        """return current temp attribute, representing the current temp of the day.
        This is only available if forecast type is TODAY."""
        return self._current_temp

    @property
    def forecast_date(self):
        """return forecast date attribute, returns forecast date.If forecast date is not supplied,
        it returns the current date"""
        return self._forecast_date

    @forecast_date.setter
    def forecast_date(self, forecast_date):
        """Converting date from number values into string using an explicit format code.
        %a returns a weekday as an abbreviated  eg. Sat. %A returns as full weekday name string.
        %b returns month as an abbreviated name eg. Feb. %B returns full month name string
        %d returns day of the month as a zero-padded number eg 01,02,17.
        Refer to strftime() and strptime()format codes in Python documentation for more info
        on date format codes"""
        self._forecast_date = forecast_date.strftime("%a %b %d")

    @property
    def wind(self):
        """return wind attribute, info about the day's wind levels"""
        return self._wind

    @property
    def humidity(self):
        """return humidity attribute, info of humidity percentage of the day"""
        return self._humidity

    @property
    def description(self):
        """return description attribute, info of description of the day's weather eg. Sunny"""
        return self._description

    def __str__(self):
        """if forecast type is today print the day's current temp together with low and high temps.
        However if forecast type is not today just print low and high temps"""
        temperature = None
        spacing = '' * 4

        # self._low_temp represents the lowest temp of the day
        # self._high_temp the highest temp of the day

        if self._forecast_type == ForecastType.TODAY:
            temperature = (f'{spacing} {self._current_temp}\xb0\n'  # xb0 is for the degree celsius symbol
                           f'{spacing} High {self._high_temp}\xb0 /'
                           f'Low {self._low_temp}\xb0')

        else:
            temperature = (f'{spacing} {self._high_temp}\xb0 /'
                           f'Low {self._low_temp}\xb0 ')

        return (f'>> {self._forecast_date}\n'
                f'{temperature}\n'
                f'({self._description})\n'
                f'{spacing}Wind:'
                f'{self._wind}  / Humidity: {self._humidity}\n')
