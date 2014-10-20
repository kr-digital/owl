"""
    Owl local storage
"""
import os
import re
import hashlib
from owl.storage.core import Core
from owl.storage.engines import AbstractStorage
from owl import settings, error_codes
from owl.answer import Answer
from owl.storage import processors, commands
from shutil import copyfileobj, copyfile, rmtree


class LocalStorage(AbstractStorage):
    """Local storage"""

    def put_file(self, file):
        """Put file into storage

        :param file: file to save
        :type file: file
        :return: owl.Answer
        """
        # Build path
        storage_dir = os.path.join(settings.STORAGE_ENGINE_LOCAL_DATA_PATH, self.client)
        if not os.path.exists(storage_dir):
            os.mkdir(storage_dir)

        # Get folders
        h = hashlib.md5()
        h.update(file.name.encode('utf-8'))
        md5 = h.hexdigest()

        # Check for first subfolder
        storage_dir = os.path.join(storage_dir, md5[0])
        if not os.path.exists(storage_dir):
            os.mkdir(storage_dir)

        # Check for second subfolder
        storage_dir = os.path.join(storage_dir, md5[1])
        if not os.path.exists(storage_dir):
            os.mkdir(storage_dir)

        # Prepare filename
        file.name = self.prepare_filename(file.name)

        # Check filename for duplicates
        filename = file.name
        dst = os.path.join(storage_dir, filename)
        i = 1
        while os.path.exists(dst):
            filename = str(i) + '_' + file.name
            dst = os.path.join(storage_dir, filename)
            i += 1

        # Open file
        dst = open(dst, 'wb')
        try:
            copyfileobj(file, dst, 16384)
        finally:
            dst.close()

        # TODO: Check for filesize after copying

        a = Answer()
        a.set_result(True)
        a.set_output_file(md5[0] + '/' + md5[1] + '/' + filename)
        return a

    def get_file(self, filename, filters='', force=False):
        """Get file from storage

        :param filename: filename at storage
        :type filename: str
        :param filters: transformation filters
        :type filters: str
        :param force: force cache ignore
        :type force: bool
        :return: owl.Answer
        """
        # Answer
        a = Answer()
        a.set_request_file(filename)
        a.set_request_filters(filters)

        # Normalize filename
        filename = self.normalize_filename(filename)

        # Check filename
        filepath = filename.split('/')
        r = re.compile(r'^[0123456789abcdef]$')
        if len(filepath) != 3 or not r.match(filepath[0]) or not r.match(filepath[1]):
            a.set_result(False)
            a.set_err_code(error_codes.GET_FILENAME_INCORRECT)
            return a

        # Storage dir
        storage_dir = os.path.join(settings.STORAGE_ENGINE_LOCAL_DATA_PATH, self.client)

        # Original file
        file_original = os.path.join(storage_dir, filename)

        # Check original file for existence
        if not os.path.exists(file_original):
            a.set_result(False)
            a.set_err_code(error_codes.GET_FILE_NOT_FOUND)
            return a

        # Get file
        if filters:
            # Check for cache directory
            cache_dir = os.path.join(storage_dir, 'cache')
            if not os.path.exists(cache_dir):
                os.mkdir(cache_dir)

            # Check for first subfolder
            subfolder_dir = os.path.join(cache_dir, filepath[0])
            if not os.path.exists(subfolder_dir):
                os.mkdir(subfolder_dir)

            # Check for second subfolder
            subfolder_dir = os.path.join(subfolder_dir, filepath[1])
            if not os.path.exists(subfolder_dir):
                os.mkdir(subfolder_dir)

            # Check for file folder
            file_dir = os.path.join(cache_dir, filename)
            if not os.path.exists(file_dir):
                os.mkdir(file_dir)

            # Parse filters
            parser = processors.FilterParser(filters)

            # Result filename
            file_result_path = self.build_file_result_path(file_dir, filters, filename, parser.get_commands())
            file_result_name = self.build_file_result_name(filters, filename, parser.get_commands())

            # Check if result file already exists
            if os.path.exists(file_result_path) and not force:
                if settings.DEBUG:
                    print('   File {0} has taken from cache'.format(file_result_name))
                a.set_result(True)

                a.set_output_file(file_result_name)
                a.set_output_filesize(os.path.getsize(file_result_path))
                return a

            # Copy result file
            copyfile(file_original, file_result_path)

            # TODO: check for filesize after copying

            # Define operator to use
            if Core.is_vector(file_original):
                op = settings.STORAGE_VECTOR_OPERATOR
            else:
                op = settings.STORAGE_IMAGE_OPERATOR

            # Get image operator
            operator = processors.get_image_operator(file_result_path, op)

            # Get image processor
            processor = processors.ImageProcessor()

            # Add commands
            for c in parser.get_commands():
                if settings.DEBUG:
                    print('  Added command {0} on file {1} with args {2}'.format(c['command'], filename, c['args']))
                if c['command'] == 'resample':
                    processor.add_command(commands.ResampleImageCommand(operator, *c['args']))
                elif c['command'] == 'convert':
                    processor.add_command(commands.ConvertImageCommand(operator, *c['args']))
                elif c['command'] == 'saturate':
                    processor.add_command(commands.SaturateImageCommand(operator, *c['args']))
                elif c['command'] == 'blur':
                    processor.add_command(commands.BlurImageCommand(operator, *c['args']))
                elif c['command'] == 'bright':
                    processor.add_command(commands.BrightImageCommand(operator, *c['args']))

            # Execute all the commands
            processor.execute_commands()

            a.set_result(True)
            a.set_output_file(operator.a_filename)
            a.set_output_filesize(os.path.getsize(operator.filename))
            return a
        else:
            a.set_result(True)
            a.set_output_file(filename)
            return a

    def del_file(self, filename):
        """Del file from storage

        :param filename: filename at storage
        :type filename: str
        :return: owl.Answer
        """
        # Storage dir
        storage_dir = os.path.join(settings.STORAGE_ENGINE_LOCAL_DATA_PATH, self.client)

        # Original file
        file_original = os.path.join(storage_dir, filename)

        # Remove original file
        if settings.DEBUG:
            print('Remove file:', file_original)
        os.unlink(file_original)

        # Remove for cache directory
        cache_dir = os.path.join(storage_dir, 'cache', filename)
        if settings.DEBUG:
            print('Remove dir:', cache_dir)
        rmtree(cache_dir, True)

        # Answer
        a = Answer()
        a.set_request_file(filename)
        a.set_result(True)
        return a

    def build_file_result_path(self, file_dir, filters, filename, commands):
        """ Build path to result file
        :param file_dir: file directory
        :type file_dir: str
        :param filters: processing filters
        :type filters: str
        :param filename: filename
        :type filename: str
        :return: str
        """

        return os.path.join(file_dir, filters.replace('|', '_') + os.path.splitext(filename)[1] + self.extract_convert_ext(commands))

    def build_file_result_name(self, filters, filename, commands):
        """ Build result filename
        :param filters: processing filters
        :type filters: str
        :param filename: filename
        :type filename: str
        :param commands: list of commands
        :type commands: list
        :return: str
        """

        return os.path.join('cache/', filename, filters.replace('|', '_') + os.path.splitext(filename)[1] + self.extract_convert_ext(commands))

    def extract_convert_ext(self, commands):
        """ Extracts file extention converts to
        :param commands: list of commands
        :type commands: list
        :return: str
        """

        ext = ""

        commands.reverse()
        for c in commands:
            if c['command'] == 'resample':
                if c['args'][3] is not None:
                    ext = c['args'][3]
                break
            elif c['command'] == 'convert':
                ext = c['args'][0]
                break

        return ext
