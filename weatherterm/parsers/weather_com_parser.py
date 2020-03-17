import re
from bs4 import BeautifulSoup
from weatherterm.core import ForecastType
from weatherterm.core import UnitConverter
from weatherterm.core import Unit
from weatherterm.core import Request
from weatherterm.core import Forecast
from weatherterm.core import Mapper


class WeatherComParser:

    def __init__(self):
        self._forecast = {
            ForecastType.TODAY: self._today_forecast,
            ForecastType.FIVEDAYS: self._five_and_ten_days_forecast,
            ForecastType.TENDAYS: self._five_and_ten_days_forecast,
            ForecastType.WEEKEND: self._weekend_forecast,
        }
        # the URL template to perform requests to weather website
        self._base_url = 'http://weather.com/weather/{forecast}/1/{area}'
        self._request = Request(self._base_url)  # attribute for Request class
        self._temp_regex = re.compile('([0-9]+)\D{,2}([0-9]+)')
        self._only_digits_regex = re.compile('[0-9]+')
        # attribute for unit conversion
        self._unit_converter = UnitConverter(Unit.FAHRENHEIT)  # default unit is set to Fahrenheit

    def _get_data(self, container, search_items):  # container is a DOM element in the HTML
        #  search_items is a dictionary where key is the class and value is the type of HTML element
        scraped_data = {}

        for key, value in search_items.items():

            result = container.find(value, class_=key)

            data = None if result is None else result.get_text()  # .get_text() to extract text from DOM element

            if data is not None:
                scraped_data[key] = data  #

        return scraped_data

    def _parse(self, container, criteria):
        # items are the children of the section container in the website that house a lot of the web info
        # criteria is the dictionary received in _today_forecast method
        results = [self._get_data(item, criteria)
                   for item in container.children]

        return [result for result in results if result]

    def _clear_str_number(self, str_number):
        """To return only digits"""
        result = self._only_digits_regex.match(str_number)
        return '--' if None else result.group()

    def _get_humidity_and_weather(self, content):
        """The information for humidity and weather can be traced from the content tag to td tag which
        contains a list of tr tags when the weathercom website is inspected """
        data = tuple(item.td.span.get_text()
                     for item in content.table.tbody.children)  # the tr tags are the children of tbody

        # the first two tr tags are the ones with info on humidity and weather so we retrieve them
        return data[:2]

    def _parse_list_forecast(self, content, args):

        # data for 5-day and 10-day have the same CSS class and DOM elements
        criteria = {
            'date-time': 'span',  # element contains string containing day of the week
            'day-detail': 'span',  # element contains string with date
            'description': 'td',  # element contains description of weather
            'temp': 'td',  # element contains low temp and high temp
            'wind': 'td',  # element contains wind information
            'humidity': 'td',  # humidity contains humidity info
        }

        bs = BeautifulSoup(content, 'html.parser')
        # CSS class and DOM element where you find data for 5 and 10 day forecasts
        forecast_data = bs.find('table', class_='twc-table')
        container = forecast_data.tbody

        return self._parse(container, criteria)

    def _prepare_data(self, results, args):
        forecast_data = []

        self._unit_converter.dest_unit = args.unit

        for item in results:
            match = self._temp_regex.search(item['temp'])
            if match is not None:
                high_temp, low_temp = match.groups()

            try:
                dateinfo = item['weather-cell']
                date_time, day_detail = dateinfo[:3], dateinfo[3:]
                item['day-detail'] = day_detail
            except KeyError:
                pass

            day_forecast = Forecast(self._unit_converter.convert(item['temp']), item['humidity'], item['wind'],
                                    high_temp=self._unit_converter.convert(high_temp),
                                    low_temp=self._unit_converter.convert(low_temp), description=
                                    item['description'].strip(),
                                    forecast_data=f'{item["date-time"]} {item["day-detail"]}',
                                    forecast_type=self._forecast_type)

            forecast_data.append(day_forecast)

        return forecast_data

    def _today_forecast(self, args):
        """returns weather parses for the day"""
        # contains the DOM elements that want to find in the HTML of the weather website for today's scraping
        # key is the name of the CSS class and value is the type of HTML
        criteria = {
            'today_nowcard-temp': 'div',  # CSS class containing current temperature
            'today_nowcard-phrase': 'div',  # CSS class containing weather conditions text for description
            'today_nowcard-hilo': 'div',  # CSS class containing highest and lowest temperature
        }

        content = self._request.fetch_data(args.area_code, args.forecast_option.value)

        bs = BeautifulSoup(content, 'html.parser')  # as bs object of the page is returned
        # container is the section tag on weathercom website that holds most of the info on weather
        container = bs.find('section', class_='today_nowcard-container')

        # to find elements in children or subtags of container that are in criteria to retrieve/scrape them
        weather_conditions = self._parse(container, criteria)

        # if len of weather_conditions is less than 1, no info was obtained or scraped
        if len(weather_conditions) < 1:
            raise Exception('Could not parse weather for today')

        weather_info = weather_conditions[0]
        temp_regex = re.compile(('H\s+(\d+|\-{,2}).+'
                                 'L\s+(\d+|\-{,2})'))
        temp_info = temp_regex.search(weather_info['today_nowcard-hilo'])
        high_temp, low_temp = temp_info.groups()

        # getting wind and humidity info
        side = container.find('div', class_='today_nowcard-sidecar')
        humidity, wind = self._get_humidity_and_weather(side)

        # getting current temp
        current_temperature = self._clear_str_number(weather_info['today_nowcard-temp'])
        # set default unit to the value of args.unit attribute
        self._unit_converter.dest_unit = args.unit

        today_forecast = Forecast(self._unit_converter.convert(current_temperature), humidity, wind,
                                  self._unit_converter.convert(high_temp), self._unit_converter.convert(low_temp),
                                  description=weather_info['today_nowcard-phrase'])

        # return today_forecast object as a list
        return [today_forecast]

    def _five_and_ten_day_forecast(self, args):
        content = self._request.fetch_data(args.forest_option.value, args.area_code)
        results = self._parse_list_forecast(content, args)
        return self._prepare_data(results)

    def _weekend_forecast(self, args):
        criteria = {
            'weather-cell': 'header',
            'temp': 'p',
            'weather-phrase': 'h3',
            'wind-conditions': 'p',
            'humidity': 'p'
        }

        mapper = Mapper()
        mapper.remap_key('wind-conditions', 'wind')
        mapper.remap_key('weather-phrase', 'description')

        content = self._request.fetch_data(args.forecast_option.value, args.area_code)
        bs = BeautifulSoup(content, 'html.parser')
        forecast_data = bs.find('article', class_='ls-mod')
        container = forecast_data.div.div

        partial_results = self._parse(container, criteria)
        results = mapper.remap(partial_results)
        return self._prepare_data(results, args)

    def run(self, args):
        self._forecast_type = args.forecast_option
        forecast_function = self._forecast[args.forecast_option]
        return forecast_function(args)
