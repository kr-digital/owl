"""
    Owl image processors
"""
from abc import ABCMeta, abstractmethod
import re


def get_image_operator(f, t='imagemagick'):
    """Image operator factory

    :param f: path to image
    :type f: str
    :param t: Type of operator
    :type t: str
    :return: AbstractImageOperator
    """
    if t == 'imagemagick':
        from owl.storage.processors.imagemagick import Imagemagick

        return Imagemagick(f)
    else:
        from owl.storage.processors.imagemagick import Imagemagick

        return Imagemagick(f)


class FilterParser:
    """Filter parser"""

    # List of commands
    __commands = []

    def __init__(self, filters):
        """Constructor

        :param filters: string of request filters
        :type filters: str
        """
        self.__commands = []
        self.__parse(filters)

    def __parse(self, filters):
        """Parse filters to gain list of commands

        :param filters: string of request filters
        :type filters: str
        """
        for c in filters.split('|'):
            # Resample command
            m = re.compile(r'^w([0-9]+)h([0-9]+)(fit|fill)?$').match(c)
            if m:
                self.__commands.append({'command': 'resample', 'args': m.groups()})
                continue

            # Saturate command
            m = re.compile(r'^sat([0-9-]+)$').match(c)
            if m:
                self.__commands.append({'command': 'saturate', 'args': m.groups()})
                continue

    def get_commands(self):
        """Get all the commands

        :return: list
        """
        return self.__commands


class ImageProcessor:
    """Owl image processor"""

    # List of commands
    __commands = []

    def __init__(self):
        self.__commands = []

    def add_command(self, command):
        """Add command to stack

        :param command: command to execute
        :type command: AbstractImageCommand
        """
        self.__commands.append(command)

    def execute_commands(self):
        """Execute all the commands and clean the list of commands"""
        for c in self.__commands:
            c.execute()
        pass


class AbstractImageOperator:
    """Abstract image processor"""
    __metaclass__ = ABCMeta

    # Path to filename
    __filename = ''

    @property
    def filename(self):
        """Get filename

        :return: str
        """
        return self.__filename

    def __init__(self, filename):
        """Constructor

        :param filename: path to image
        :type filename: str
        """
        self.__filename = filename

    @abstractmethod
    def resample(self, width, height, crop):
        """Resample image

        :param width: new image width
        :type width: int
        :param height: new image width
        :type height: int
        :param crop: crop method
        :type crop: str
        """

    @abstractmethod
    def saturate(self, percent):
        """Saturate image

        :param percent: percent of saturation
        :type percent: int
        """