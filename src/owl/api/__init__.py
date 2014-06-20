"""
    OWL API module
"""

from flask import request
from owl import settings, core, error_codes
from owl.api import formats
from owl.answer import Answer


def authenticate(f):
    """Do an authentication decorator"""
    def wrapper(*args, **kwargs):
        try:
            client = request.headers['client']
        except KeyError:
            a = Answer()
            a.set_result(False)
            a.set_err_code(error_codes.AUTH_NO_CLIENT)
            return make_answer(a)

        try:
            token = request.headers['token']
        except KeyError:
            a = Answer()
            a.set_result(False)
            a.set_err_code(error_codes.AUTH_NO_TOKEN)
            return make_answer(a)

        if not core.check_token(client, token):
            a = Answer()
            a.set_result(False)
            a.set_err_code(error_codes.AUTH_WRONG_CREDENTIALS)
            return make_answer(a)

        return f(*args, **kwargs)
    return wrapper


def make_answer(a):
    """Make an answer and return it

    :param a: owl response
    :type a: owl.Answer
    :return: flask.Response
    """
    fmt = formats.get_formatter(settings.FORMAT)
    return fmt.make_answer(a)