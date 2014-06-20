"""
    Owl API JSON format
"""

from flask import Response
from owl.api.formats import AbstractFormatter
import json


class JSONFormatter(AbstractFormatter):
    """Owl JSON formatter"""

    @staticmethod
    def make_answer(answer):
        """Make an JSON answer

        :param answer: owl response
        :type answer: owl.Answer[]
        :return: flask.Response
        """
        if isinstance(answer, list):
            return Response(json.dumps({a: answer[a].dump_data() for a in range(len(answer))}), mimetype='application/json')
        else:
            return Response(json.dumps(answer.dump_data()), mimetype='application/json')