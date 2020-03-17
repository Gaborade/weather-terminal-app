from weatherterm.core import Unit
from argparse import Action


class SetUnitAction(Action):
    """Creating a custom defined action"""

    def __call__(self, parser, namespace, values, option_string=None):
        """the SetUnitAction inherits from the argparse.Action class. It overrides the call method,
        when the argument value is passed. This will be set to the destination attribute of the argparse argument"""
        # parser is an instance of Argument passer
        # namespace is an instance of argparser.Namespace. It is a simple class that all attributes defined in the
        # in the ArgumentPasser object
        unit = Unit[values.upper()]
        #  setattr contains  setattr(__object, __name, __value)
        setattr(namespace, self.dest, unit)
