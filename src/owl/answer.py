"""
    OWL Answer
"""


class Answer:
    """OWL answer"""

    def __init__(self):
        """Constructor"""
        self.__result = True
        self.__err_code = 0
        self.__output_file = ''
        self.__output_filesize = 0
        self.__request_file = ''
        self.__request_filters = ''

    def set_result(self, value):
        """Set result

        :param value: result
        :type value: bool
        """
        self.__result = value

    def set_err_code(self, value):
        """Set error code

        :param value: error code
        :type value: int
        """
        self.__err_code = value

    def set_output_file(self, value):
        """Set file

        :param value: file
        :type value: str
        """
        self.__output_file = value

    def get_output_file(self):
        """Get output file

        :return: str
        """
        return self.__output_file

    def set_output_filesize(self, value):
        """Set filesize

        :param value: filesize
        :type value: int
        """
        self.__output_filesize = value

    def set_request_file(self, value):
        """Set request file

        :param value: request file
        :type value: str
        """
        self.__request_file = value

    def set_request_filters(self, value):
        """Set request filters

        :param value: request filters
        :type value: str
        """
        self.__request_filters = value

    def dump_data(self):
        """Dumps answer data and resets state

        :return: dict
        """

        data = {'result': self.__result}

        if self.__err_code:
            data['err_code'] = self.__err_code

        if self.__output_file:
            data['output_file'] = self.__output_file

        if self.__output_filesize:
            data['output_filesize'] = self.__output_filesize

        if self.__request_file:
            data['request_file'] = self.__request_file

        if self.__request_filters:
            data['request_filters'] = self.__request_filters

        # Reset state
        self.reset()

        return data

    def reset(self):
        """Resets answer"""
        self.__init__()