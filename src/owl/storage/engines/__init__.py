"""
    Owl storage engines
"""
from abc import ABCMeta, abstractmethod
import os
import re


def get_engine(t='local'):
    """Engine factory

    :param t: Type of engine
    :type t: str
    :return: LocalStorage
    """
    if t == 's3':
        from owl.storage.engines.local import LocalStorage

        return LocalStorage()
    else:
        from owl.storage.engines.s3 import S3Storage

        return S3Storage()


class AbstractStorage:
    """Abstract base class of storage"""
    __metaclass__ = ABCMeta

    # Storage client
    __client = ''

    @property
    def client(self):
        """Get client

        :return: str
        """
        return self.__client

    @client.setter
    def client(self, value):
        """Set client

        :param value: client
        :type value: str
        """
        self.__client = value

    @client.deleter
    def client(self):
        """Delete client"""
        del self.__client

    @abstractmethod
    def put_file(self, file, watermark=False):
        """Put file into storage

        :param file: file to save
        :type file: file
        :param watermark: apply watermark
        :type watermark: bool
        :return: owl.Answer
        """

    @abstractmethod
    def get_file(self, name, filters='', force=False):
        """Get file from storage

        :param name: filename at storage
        :type name: str
        :param filters: transformation filters
        :type filters: str
        :param force: force cache ignore
        :type force: bool
        :return: owl.Answer
        """

    @abstractmethod
    def del_file(self, name):
        """Del file from storage

        :param name: filename at storage
        :type name: str
        :return: owl.Answer
        """

    @abstractmethod
    def get_real_file_path(self, name):
        """Get real file path

        :param name: filename at storage
        :type name: str
        :return: Response
        """

    def prepare_filename(self, filename):
        """Prepare filename by removing and replacing wrong characters

        :param filename: the filename to prepare
        :type filename: str
        :return: str
        """
        # Transliterate
        filename = self.transliterate_filename(filename)

        # Normalize
        filename = self.normalize_filename(filename)

        # Replace path separators
        for sep in os.path.sep, os.path.altsep:
            if sep:
                filename = filename.replace(sep, ' ')

        # Replace
        filename = str(re.compile(r'[^A-Za-z0-9_.-]').sub('', '_'.join(filename.split()))).strip('._')

        return filename

    @staticmethod
    def normalize_filename(filename):
        """Normalize filename

        :param filename: the filename to prepare
        :type filename: str
        :return: str
        """
        from unicodedata import normalize
        return str(normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii'))


    @staticmethod
    def transliterate_filename(filename):
        """Transliterate filename

        :param filename: the filename to transliterate
        :type filename: str
        :return: str
        """
        capital_letters = {u'А': u'A',
                           u'Б': u'B',
                           u'В': u'V',
                           u'Г': u'G',
                           u'Д': u'D',
                           u'Е': u'E',
                           u'Ё': u'E',
                           u'З': u'Z',
                           u'И': u'I',
                           u'Й': u'Y',
                           u'К': u'K',
                           u'Л': u'L',
                           u'М': u'M',
                           u'Н': u'N',
                           u'О': u'O',
                           u'П': u'P',
                           u'Р': u'R',
                           u'С': u'S',
                           u'Т': u'T',
                           u'У': u'U',
                           u'Ф': u'F',
                           u'Х': u'H',
                           u'Ъ': u'',
                           u'Ы': u'Y',
                           u'Ь': u'',
                           u'Э': u'E'}

        capital_letters_transliterated_to_multiple_letters = {u'Ж': u'Zh',
                                                              u'Ц': u'Ts',
                                                              u'Ч': u'Ch',
                                                              u'Ш': u'Sh',
                                                              u'Щ': u'Sch',
                                                              u'Ю': u'Yu',
                                                              u'Я': u'Ya'}

        lower_case_letters = {u'а': u'a',
                              u'б': u'b',
                              u'в': u'v',
                              u'г': u'g',
                              u'д': u'd',
                              u'е': u'e',
                              u'ё': u'e',
                              u'ж': u'zh',
                              u'з': u'z',
                              u'и': u'i',
                              u'й': u'y',
                              u'к': u'k',
                              u'л': u'l',
                              u'м': u'm',
                              u'н': u'n',
                              u'о': u'o',
                              u'п': u'p',
                              u'р': u'r',
                              u'с': u's',
                              u'т': u't',
                              u'у': u'u',
                              u'ф': u'f',
                              u'х': u'h',
                              u'ц': u'ts',
                              u'ч': u'ch',
                              u'ш': u'sh',
                              u'щ': u'sch',
                              u'ъ': u'',
                              u'ы': u'y',
                              u'ь': u'',
                              u'э': u'e',
                              u'ю': u'yu',
                              u'я': u'ya'}

        capital_and_lower_case_letter_pairs = {}

        for capital_letter, capital_letter_translit in capital_letters_transliterated_to_multiple_letters.items():
            for lowercase_letter, lowercase_letter_translit in lower_case_letters.items():
                capital_and_lower_case_letter_pairs[u"%s%s" % (capital_letter, lowercase_letter)] = u"%s%s" % (
                    capital_letter_translit, lowercase_letter_translit)

        for dictionary in (capital_and_lower_case_letter_pairs, capital_letters, lower_case_letters):
            for cyrillic_string, latin_string in dictionary.items():
                filename = filename.replace(cyrillic_string, latin_string)

        for cyrillic_string, latin_string in capital_letters_transliterated_to_multiple_letters.items():
            filename = filename.replace(cyrillic_string, latin_string.upper())

        return filename

    def parse_filters(self, filters):
        """Parse transformation filters

        :param filters: transformation filters string
        :type filters: str
        :return: dict
        """
        parsed_filters = {}
        return parsed_filters

