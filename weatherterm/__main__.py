from argparse import ArgumentParser
import sys

# we can import like from weatherterm.core import blah instead of from .. import because
# we put all the imported modules in the __ini__.py file
# the __init__.py will control all relative imports
from weatherterm.core import parser_loader
from weatherterm.core import ForecastType
from weatherterm.core import Unit
from weatherterm.core import SetUnitAction


def _validate_forecast_args(args):
    """This function will look through the attributes of the object of the ArgumentParser and
    if the forecast_option attribute is none, an error message is printed out and program exited"""
    if args.forecast_option is None:
        err_msg = """ One of these arguments must be used: 
        -td/--today, -5d/--fivedays, -10d/--tendays, -w/--weekend
        """
        print(f'{argparser.prog}: error: {err_msg}', file=sys.stderr)
        sys.exit()


# loading the parsers using the parsers from the parsers directories
parsers = parser_loader.load('./weatherterm/parsers')

# initialising the ArgumentParser class
argparser = ArgumentParser(prog='weatherterm',  # prog is a kwarg for name of terminal program
                           description='Weather info from weather on your terminal')

# an argument group which will gather all the required arguments that the app needs
# the args under required will be arguments that specify which parser to use and area code
required = argparser.add_argument_group('required arguments')

# usage of this piece of code to explain parameters of ArgumentParser
# -p, --parser are the flags. User passes a value to this argument using -p or --parser
# eg/ --parser WeatherComParser

# choices params provide a list of values for the argument we are creating. Returning a list of parser names
# required param is a boolean value of whether the argument is a required one or not

# dest specifies the name of the attribute to be added to the parser argument
# when parser_args() function is run, the object returned will contain an attribute called parser with value
# that was passed

# help can be accessed using -h or --help flags
required.add_argument('-p', '--parser', choices=parsers.keys(), required=True,
                      dest='parser', help="""Specify which parser is going to be used to scrape
                      'weather information""")  # parser argument to specify which weather parser you want to use
# it is a required argument


# the values of the of the Temperature Unit enums so users can select which temp to use
unit_values = [name.title() for name, value in Unit.__members__.items()]  # title function to make only the first
# letter a capital letter

# argparser to choose temperature unit.
required.add_argument('-u', '--u', choices=unit_values, required=False, action=SetUnitAction,
                      dest='unit', help='Specify the unit that will be used to display temperature')

# argparser for area code. This has been added as a required argument.
required.add_argument('-a', '--areacode', required=True, dest='area_code',
                      help='The code area to get the weather broadcast from. It can be obtained'
                           'at https://weather.com')

# argparser to display version of weatherterm
argparser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

# argparser to display weather stats for current day
# actions param are bound to arguments and can perform a plethora of things
# most actions in the argparse module are to store values in the parse results object attributes


argparser.add_argument('-td', '--today', dest='forecast_option',
                       action='store_const', const=ForecastType.TODAY,  # const specifies the constant default value
                       help='Show the weather forecast for the current day')

# argparser for five day reading of weather
argparser.add_argument('-5d', '--fivedays', dest='forecast_option', action='store_const',
                       const=ForecastType.FIVEDAYS, help='Shows the weather forecast for the next 5 days')

# argparser for ten day reading of weather
argparser.add_argument('-10d', '--tenday', dest='forecast_option', action='store_const',
                       const=ForecastType.TENDAYS, help='Shows the weather forecast for the next 10 days')

# argparser for the weekend reading of weather
argparser.add_argument('-w', '--weekend', action='store_const', dest='forecast_option', const=ForecastType.WEEKEND,
                       help='Show the weather forecast for the next or current weekend')


args = argparser.parse_args()  # parser_args is an in-built function inside the argparse module
# it will return an object with the dest params of the parse arguments becoming attributes of a Namespace class
# it will look something like this: Namespace(area_code=None, fields=None, forecast_type=None, parser=None,
# unit=None)

_validate_forecast_args(args)

# after the _validate_forecast_args function is run with no problem the parser attributes are retrieved
# and used as keys to load for the parser classes dynamically in the parsers dictionary
# args.parser will be name of the selected parser chosen by the user
parser_class = parsers[args.parser]

# the values in the parsers dictionary are a class type so it has to be initialised
parser = parser_class()
results = parser.run(args)  # the parser classes have a run method

for result in results:
    print(result)
