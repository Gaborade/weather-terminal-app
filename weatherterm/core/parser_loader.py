import os
import inspect
import re

"""In order to make the app flexible and reusable, every website will have a different parser.
parser_loader.py searches for parsers inside the weatherterm.parsers directory and loads them without requiring any other
changes.
The files loaded will be the parser files. Parser files will have a suffix of 'parsers' added to filename
eg. openforecast_parser.py for identification. Files beginning with double underscores will not be retrieved"""


def _get_parser_list(dirname):
    """The function returns the list of items/files residing in weatherterm/parsers directory
    if only it doesn't start with a double underscore."""
    # .py extension replaced with an empty string since later they will be used for import
    # and __import__() takes only the filename as a string and not the extension.
    files = [file.replace('.py', '')
             for file in os.listdir(dirname)  # os.listdir lists the items of a directory as a list
             if not file.startswith('__')]

    return files


def _import_parsers(parser_files):
    # regex to match file which has a suffix of 'parser'
    m = re.compile('.+parser$', re.IGNORECASE)  # make string case insensitive

    # import modules in parser directory using built in module function __import__(name, globals, local, fromlist,
    # level)
    # name takes the package path of the module
    # globals(), locals() import the globals and locals of the said module fromlist refers to the string
    # of actual module being imported from the package directory(in this case parser_files)
    # level specifies whether to use absolute imports or relative imports. 0 is absolute import and 1
    # and above signify relative imports

    # import all modules in weatherterm/parsers directory
    _modules = __import__('weatherterm.parsers',
                          globals(), locals(), parser_files, 0)

    # getmembers by default returns a tuple if object is a module and has a parser suffix
    # m.match matches if 'parser' substring in module string
    _parsers = [(name, data) for name, data in inspect.getmembers(_modules) if
                inspect.ismodule(name) and m.match(data)]

    _classes = dict()

    # dictionary comprehension
    # getmembers to find classes within parser modules and match to find only classes which have a 'parser' substring
    # then store name of class and class object in a dictionary.
    for name, data in _parsers:
        _classes.update({name: data for name, data in
                         inspect.getmembers(data) if inspect.isclass(data) and m.match(name)})

    return _classes


def load(dirname):
    parser_files = _get_parser_list(dirname)
    return _import_parsers(parser_files)
