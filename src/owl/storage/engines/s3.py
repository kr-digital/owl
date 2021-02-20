"""
    Owl s3 storage
"""
import os
import re
import boto3
import uuid
import hashlib
import tempfile
from owl.storage.core import Core
from owl.storage.engines import AbstractStorage
from owl import settings, error_codes
from owl.answer import Answer
from owl.storage import processors, commands
from owl.storage.processors import Optimizer
from shutil import copyfileobj


class S3Storage(AbstractStorage):
    """S3 storage"""

    def __init__(self):
        """Constructor"""

        self.__session = boto3.session.Session()
        self.__s3 = self.__session.client(
            service_name='s3',
            endpoint_url=settings.STORAGE_ENGINE_S3_ENDPOINT_URL
        )

    def put_file(self, file, watermark=False):
        """Put file into storage

        :param file: file to save
        :type file: file
        :param watermark: apply watermark
        :type watermark: bool
        :return: owl.Answer
        """
        # Get folders
        h = hashlib.md5()
        h.update(file.name.encode('utf-8'))
        md5 = h.hexdigest()

        # Prepare filename
        ext = os.path.splitext(file.name)[1].lower()
        if settings.STORAGE_NAMING_STRATEGY == 'uuid':
            file.name = str(uuid.uuid4()) + ext
        else:
            file.name = self.prepare_filename(file.name)
            if '.' + file.name == ext:
                file.name = str(uuid.uuid4()) + ext

        # Check filename for duplicates
        filename = file.name
        s3_items = self.__s3.list_objects(Bucket=self.client, Prefix=os.path.join(md5[0], md5[1], filename))
        i = 1
        while s3_items.get('Contents') is not None:
            filename = str(i) + '_' + file.name
            s3_items = self.__s3.list_objects(Bucket=self.client, Prefix=os.path.join(md5[0], md5[1], filename))
            i += 1

        # Process original
        if settings.STORAGE_PROCESS_ORIGINALS_FILTER:
            tmp_file = tempfile.NamedTemporaryFile()
            tmp_file.write(file.read())
            tmp_file.seek(0)

            self.optimize_file(tmp_file.name, settings.STORAGE_PROCESS_ORIGINALS_FILTER)

            file = tmp_file

        # Apply watermark
        if watermark:
            # Save original
            file.seek(0)
            try:
                copyfileobj(file, file, 16384)
            finally:
                file.close()

            operator = processors.get_image_operator(file, settings.STORAGE_IMAGE_OPERATOR)
            watermark_file = os.path.join(settings.STORAGE_ENGINE_LOCAL_DATA_PATH, self.client, settings.WATERMARK['file'])
            operator.watermark(watermark_file)

        # Upload to S3
        self.__s3.upload_fileobj(file, self.client, os.path.join(md5[0], md5[1], filename))

        # Delete tmp_file
        file.close()

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

        # Check original file for existence
        s3_items = self.__s3.list_objects(Bucket=self.client, Prefix=filename)
        if s3_items.get('Contents') is None:
            a.set_result(False)
            a.set_err_code(error_codes.GET_FILE_NOT_FOUND)
            return a

        # Get file
        if filters:
            # Parse filters
            parser = processors.FilterParser(filters)

            # Result filename
            file_result_name = self.build_file_result_name(filters, filename, parser.get_commands())

            # Check if result file already exists
            s3_items = self.__s3.list_objects(Bucket=self.client, Prefix=file_result_name)
            if s3_items.get('Contents') is not None and not force:
                if settings.DEBUG:
                    print('   File {0} has taken from cache'.format(file_result_name))
                a.set_result(True)

                a.set_output_file(file_result_name)
                a.set_output_filesize(s3_items.get('Contents')[0]['Size'])
                return a

            # Download file to tmp folder
            get_object_response = self.__s3.get_object(Bucket=self.client, Key=filename)
            tmp_file = tempfile.NamedTemporaryFile()
            tmp_file.write(get_object_response['Body'].read())
            tmp_file.seek(0)

            # Define operator to use
            if Core.is_vector(tmp_file.name):
                op = settings.STORAGE_VECTOR_OPERATOR
            else:
                op = settings.STORAGE_IMAGE_OPERATOR

            # Get image operator
            operator = processors.get_image_operator(tmp_file.name, op)

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
                elif c['command'] == 'watermark':
                    watermark_file = os.path.join(settings.STORAGE_ENGINE_LOCAL_DATA_PATH, self.client, settings.WATERMARK['file'])
                    processor.add_command(commands.WatermarkImageCommand(operator, watermark_file))

            # Execute all the commands
            processor.execute_commands()

            Optimizer.optimize(operator.filename)
            tmp_file_size = os.path.getsize(tmp_file.name)

            # Upload to S3
            self.__s3.upload_fileobj(tmp_file, self.client, file_result_name)

            # Delete tmp_file
            tmp_file.close()

            a.set_result(True)
            a.set_output_file(file_result_name)
            a.set_output_filesize(tmp_file_size)
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

        list_to_delete = [{'Key': filename}]

        s3_items = self.__s3.list_objects(Bucket=self.client, Prefix=os.path.join('cache', filename))
        if s3_items.get('Contents') is not None:
            for key in s3_items.get('Contents'):
                list_to_delete.append({'Key': key['Key']})

        self.__s3.delete_objects(Bucket=self.client, Delete={'Objects': list_to_delete})

        # Answer
        a = Answer()
        a.set_request_file(filename)
        a.set_result(True)
        return a

    def get_real_file_path(self, filename):
        """Send file to client

        :param filename: filename at storage
        :type filename: str
        :return: Response
        """

        return filename

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
