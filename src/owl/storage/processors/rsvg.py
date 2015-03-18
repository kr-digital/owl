"""
    Owl rsvg processor
"""
from owl.storage.processors import AbstractImageOperator
from owl import settings
import subprocess
from shutil import copyfile
import os


class Rsvg(AbstractImageOperator):
    def watermark(self, position):
        pass

    def bright(self, percent):
        pass

    def saturate(self, percent):
        pass

    def blur(self, radius, sigma):
        pass

    def convert(self, format):
        if settings.DEBUG:
            print(
                '   Executed convert to {1} command by Rsvg on file {0}'.
                format(self.filename, format))

        tmp_file = self.create_tmp_file()

        output_file = self.filename

        r = subprocess.getoutput(
            settings.STORAGE_VECTOR_OPERATOR_CONVERT_PATH + ' ' + tmp_file + ' -a -f ' + format.replace('.', '') + ' -o '
            + output_file)

        os.unlink(tmp_file)

        self.set_filename(output_file)

    def resample(self, width, height, crop, f):
        if settings.DEBUG:
            print(
                '   Executed resample command by Rsvg on file {0} with width={1}, height={2} and crop={3}'.
                format(self.filename, width, height, crop))

        tmp_file = self.create_tmp_file()

        output_file = self.filename

        if f is None:
            f = '.svg'

        r = subprocess.getoutput(
            settings.STORAGE_VECTOR_OPERATOR_CONVERT_PATH + ' ' + tmp_file + ' -a -f ' + f.replace('.', '') + ' -w '
            + width + ' -h ' + height + ' -o ' + output_file)

        os.unlink(tmp_file)

        self.set_filename(output_file)

    def create_tmp_file(self):
        """ Creates a temporary file for performing modifications
        """

        tmp_filename = 'tmp_' + os.path.basename(self.filename)

        tmp_file = os.path.join(os.path.dirname(self.filename), tmp_filename)

        copyfile(self.filename, tmp_file)

        return tmp_file
