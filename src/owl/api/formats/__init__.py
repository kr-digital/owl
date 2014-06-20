"""
    Owl answer formats
"""
from abc import ABCMeta, abstractmethod


def get_formatter(t='JSON'):
    """Formatter factory

    :param t: Type of format
    :type t: str
    :return: JSONFormatter
    """
    if t == 'JSON':
        from owl.api.formats.json import JSONFormatter
        return JSONFormatter()
    else:
        from owl.api.formats.json import JSONFormatter
        return JSONFormatter()


class AbstractFormatter:
    """Abstract base class of formatter"""
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def make_answer(answer):
        """Make an JSON answer

        :param answer: owl response
        :type answer: owl.Answer
        :return: flask.Response
        """