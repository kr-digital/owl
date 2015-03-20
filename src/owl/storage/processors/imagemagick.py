"""
    Owl imagemagick processor
"""
from owl.storage.processors import AbstractImageOperator
from owl import settings
import subprocess


class Imagemagick(AbstractImageOperator):
    """Imagemagick operator"""

    def resample(self, width, height, crop, f):
        """Resample image

        :param width: new image width
        :type width: str
        :param height: new image width
        :type height: str
        :param crop: crop method
        :type crop: str
        :param f: convert to
        :type f: str
        """

        output_file = self.filename

        if crop is None:
            crop = 'fit'

        if settings.DEBUG:
            print(
                '   Executed resample command by Imagemagick on file {0} with width={1}, height={2} and crop={3}'.
                format(self.filename, width, height, crop))

        if crop == 'fit':
            r = subprocess.getoutput(
                settings.STORAGE_IMAGE_OPERATOR_CONVERT_PATH + ' \'' + self.filename + '\' -auto-orient -resize ' + width +
                'x' + height + ' \'' + output_file + '\'')

            if r and settings.DEBUG:
                print('    Error during processing: ', r)
        elif crop == 'fill':
            r = subprocess.getoutput(
                settings.STORAGE_IMAGE_OPERATOR_CONVERT_PATH + ' \'' + self.filename + '\' -auto-orient -resize ' + width +
                'x' + height + '^ -gravity center -extent ' + width + 'x' + height + ' \'' +
                output_file + '\'')

            if r and settings.DEBUG:
                print('    Error during processing: ', r)

        self.set_filename(output_file)

    def saturate(self, percent):
        """Saturate image

        :param percent: percent of saturation
        :type percent: str
        """

        if settings.DEBUG:
            print(
                '   Executed saturation command by Imagemagick on file {0} with percent={1}'.
                format(self.filename, percent))

        # Increase percent by 100
        percent = str(int(percent)+100)

        r = subprocess.getoutput(
            settings.STORAGE_IMAGE_OPERATOR_CONVERT_PATH + ' \'' + self.filename + '\' -modulate 100,' + percent +
            ' \'' + self.filename + '\'')

        if r and settings.DEBUG:
            print('    Error during processing: ', r)

    def blur(self, radius, sigma):
        """Saturate image

        :param radius: radius of blur
        :type radius: int
        :param sigma: sigma of blur
        :type sigma: int
        """

        if settings.DEBUG:
            print(
                '   Executed blur command by Imagemagick on file {0} with {1}x{2}'.
                format(self.filename, radius, sigma))

        r = subprocess.getoutput(
            settings.STORAGE_IMAGE_OPERATOR_CONVERT_PATH + ' \'' + self.filename + '\' -blur ' + str(radius) + 'x' + str(
                sigma) + ' \'' + self.filename + '\'')

        if r and settings.DEBUG:
            print('    Error during processing: ', r)

    def bright(self, percent):
        """Bright image

        :param percent: percent of brightness
        :type percent: str
        """

        if settings.DEBUG:
            print(
                '   Executed brightness command by Imagemagick on file {0} with percent={1}'.
                format(self.filename, percent))


        r = subprocess.getoutput(
            settings.STORAGE_IMAGE_OPERATOR_CONVERT_PATH + ' \'' + self.filename + '\' -brightness-contrast ' +
            str(percent) + ' \'' + self.filename + '\'')

        if r and settings.DEBUG:
            print('    Error during processing: ', r)

    def convert(self, format):
        """Convert image

        :param format: format to convert
        :type format: str
        """

        if settings.DEBUG:
            print(
                '   Executed convert to {1} command by Convert on file {0}'.
                format(self.filename, format))

        output_file = self.filename

        r = subprocess.getoutput(
            settings.STORAGE_IMAGE_OPERATOR_CONVERT_PATH + ' \'' + self.filename + '\' ' + ' \'' + output_file + '\'')

        self.set_filename(output_file)

    def watermark(self, watermark_file):
        """Apply watermark to image

        :param watermark_file: path to watermark file
        :type watermark_file: String
        """

        # Auto orient image
        subprocess.getoutput(
            settings.STORAGE_IMAGE_OPERATOR_CONVERT_PATH + ' \'' + self.filename + '\' -auto-orient \'' +
            self.filename + '\'')

        # Get image size
        size = subprocess.getoutput(
            settings.STORAGE_IMAGE_OPERATOR_IDENTIFY_PATH + ' -quiet -format "%wx%h" \'' + self.filename + '\'')

        if settings.DEBUG:
            print(
                '   Executed watermark {1} of size {2} file by Composite on file {0}'.
                format(self.filename, watermark_file, size))

        output_file = self.filename

        r = subprocess.getoutput(
            settings.STORAGE_IMAGE_OPERATOR_COMPOSE_PATH + ' \( \'' + watermark_file + '\' -resize ' + size + ' \) \'' +
            self.filename + '\' -gravity ' + settings.WATERMARK['position'] + ' \'' + self.filename + '\'')

        self.set_filename(output_file)