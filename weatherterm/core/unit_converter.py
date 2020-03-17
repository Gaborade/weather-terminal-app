from .unit import Unit


# the UnitConverter class has strategy pattern written all over it.
# it would be better if methods to convert temp to celsius or fahrenheit were plain functions instead of methods tied
# to a class. That way they can be used for multiple use cases

class UnitConverter:
    """By default, the temperature unit used by most sites is Fahrenheit. But we want to give users added
    functionality in being able to choose the Temperature unit of their preference"""

    def __init__(self, parser_default_unit, dest_unit=None):
        # self.dest_unit is not a protected attribute because it is the user that will set their unit of preference
        self.dest_unit = dest_unit
        self._parser_default_unit = parser_default_unit

        # since python functions are first class objects, you can store them in data structures
        # assigned the Unit Enums to the conversion functions in a dictionary
        # the temperature conversions are assigned to a dictionary with the their unit types
        self._convert_functions = {
            Unit.CELSIUS: self._to_celsius,
            Unit.FAHRENHEIT: self._to_fahrenheit,
        }

    @property
    def dest_unit(self):
        return self._dest_unit

    @dest_unit.setter
    def dest_unit(self, dest_unit):
        self._dest_unit = dest_unit

    def convert(self, temp):
        # temp value will be a string so we have to convert to an float.
        # if that fails then we just return zero right away

        try:
            temperature = float(temp)
        except ValueError:
            return 0

        # if self.dest_unit(Unit.FAHRENHEIT or Unit.CELSIUS is equal to the default parser unit, there is
        # no need for conversion.
        if self.dest_unit == self._parser_default_unit or self.dest_unit is None:
            return self._format_results(temperature)

        else:
            # else if self.dest_unit and self._parser_default_unit are different, convert the temperature based on the
            # output of self.dest_unit

            # python's power of first class functions is harnessed here again.
            # the function to convert temperatures is retrieved using a key then assigned to a variable
            # the variable through the power of first class functions again( functions can be assigned to
            # variables and the variables perform the function calls) then computes the conversion of temp
            func = self._convert_functions[self.dest_unit]
            result = func(temperature)
            return self._format_results(result)

    def _format_results(self, value):
        # if the value is an integer we return the value as an integer however if the value of temp is not an integer
        # then we format it with one decimal value
        return int(value) if value.is_integer() else f'{value:.1f}'

    def _to_celsius(self, fahrenheit_temp):
        result = (fahrenheit_temp - 32) * 5 / 9
        return result

    def _to_fahrenheit(self, celsius_temp):
        result = (celsius_temp * 9 / 5) + 32
        return result

# things i liked here
# there was a distinct feeling of a single chain of responsibility
# the functions only carried specific purposes
# convert function was broken down into 3 functions, the convert to celsius,
# convert to fahrenheit and format results and the the convert function basically called them
# i do feel the three functions could have been static methods or just normal functions
# that way they could be used for other conversion processes without being tightly coupled
# with the class UnitConverter
