"""
    Owl image processors
"""
from abc import ABCMeta, abstractmethod
from owl import settings
import re
import os
import subprocess


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
    elif t == 'librsvg':
        from owl.storage.processors.rsvg import Rsvg

        return Rsvg(f)
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
            m = re.compile(r'^w([0-9]+)h([0-9]+)(fit|fill)?(\.[A-z]+)?$').match(c)
            if m:
                self.__commands.append({'command': 'resample', 'args': m.groups()})
                continue

            # Saturate command
            m = re.compile(r'^sat([0-9-]+)$').match(c)
            if m:
                self.__commands.append({'command': 'saturate', 'args': m.groups()})
                continue

            # Blur command
            m = re.compile(r'^blur([0-9]+)x([0-9]+)$').match(c)
            if m:
                self.__commands.append({'command': 'blur', 'args': m.groups()})
                continue

            # Saturate command
            m = re.compile(r'^bright([0-9-]+)$').match(c)
            if m:
                self.__commands.append({'command': 'bright', 'args': m.groups()})
                continue

            # Convert command
            m = re.compile(r'^c(\.[A-z]+)$').match(c)
            if m:
                self.__commands.append({'command': 'convert', 'args': m.groups()})

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

    @property
    def a_filename(self):
        """Get answer filename

        :return: str
        """
        return 'cache' + self.__filename.split('cache')[1]

    def set_filename(self, filename):
        """Set filename
        :param filename: new filename
        :type filename: str
        : return: str
        """
        self.__filename = filename
        return self.filename

    def __init__(self, filename):
        """Constructor

        :param filename: path to image
        :type filename: str
        """
        self.__filename = filename

    @abstractmethod
    def resample(self, width, height, crop, f):
        """Resample image

        :param width: new image width
        :type width: int
        :param height: new image width
        :type height: int
        :param crop: crop method
        :type crop: str
        :param format: format to convert
        :type format: str
        """

    @abstractmethod
    def saturate(self, percent):
        """Saturate image

        :param percent: percent of saturation
        :type percent: int
        """

    @abstractmethod
    def blur(self, radius, sigma):
        """Blur image

        :param radius: radius of blur
        :type radius: int
        :param sigma: sigma of blur
        :type sigma: int
        """

    @abstractmethod
    def bright(self, percent):
        """Bright image

        :param percent: percent of brightness
        :type percent: int
        """

    @abstractmethod
    def convert(self, format):
        """Convert image

        :param format: convert to format
        :type format: String
        """

class Optimizer:
    """Image optimizer"""

    commands = {
        'jpg': 'jpegtran {options} -outfile \'{file}\' \'{file}\'',
        'png': 'optipng {options} \'{file}\''
    }

    @staticmethod
    def optimize(file):
        """
        Run optimize command on specific file

        :param file: path to file
        :type file: String
        """

        ext = os.path.splitext(file)[1].replace('.','').lower()

        if ext == 'jpeg':
            ext = 'jpg'

        if ext in Optimizer.commands:
            command = Optimizer.commands[ext]
            optimize_settings = settings.OPTIMIZERS[ext]

            if 'options' not in optimize_settings:
                optimize_settings['options'] = ''

            if optimize_settings['enabled']:
                print(
                '   Optimizing {0}'.
                format(file))
                return subprocess.getoutput(command.format(options=optimize_settings['options'], file=file))

        return None