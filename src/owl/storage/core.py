"""
    Owl core class
"""
import os
from owl import settings, error_codes
from owl.storage import engines
from owl.answer import Answer
from threading import Thread
from queue import Queue
from queue import Empty


class Core:
    """Storage core"""

    # Current client
    __client = None

    # Threads result
    __threads_result = []

    def __init__(self):
        """Core constructor"""
        self.__clients = settings.CLIENTS
        self.__gettersPool = Queue()

        for i in range(settings.STORAGE_WORKERS):
            _t = Thread(target=self.__threads_get_file, args=(i+1, self.__gettersPool))
            _t.setDaemon(True)
            _t.start()

    def check_token(self, client, token):
        """Check request headers for valid client and token

        :param client: API client
        :type client: str
        :param token: API token
        :type token: str
        :return: bool
        """

        # Check client
        if client not in settings.CLIENTS.keys():
            return False

        # Check client token
        if settings.CLIENTS[client] != token:
            return False

        # Set client
        self.__client = client

        return True

    def put_file(self, file):
        """Put file to storage

        :param file: file to save
        :type file: file
        :return: owl.Answer
        """
        # Check file extension
        if file.name.rsplit('.', 1)[1].lower() not in settings.ALLOWED_EXTENSIONS:
            a = Answer()
            a.set_result(False)
            a.set_err_code(error_codes.UPLOAD_WRONG_EXTENSION)
            return a

        # Check filesize
        file.seek(0, os.SEEK_END)
        if file.tell() > settings.MAX_FILESIZE:
            a = Answer()
            a.set_result(False)
            a.set_err_code(error_codes.UPLOAD_WRONG_FILESIZE)
            return a
        else:
            file.seek(0)

        # Put file
        e = engines.get_engine(settings.STORAGE_ENGINE)
        e.client = self.__client
        return e.put_file(file)

    def get_files(self, files, force=False):
        """Get files from storage

        Each element of files must be a tuple: filename and filter

        :param files: file names at storage
        :type files: list
        :param force: force cache ignore
        :type force: bool
        :return: owl.Answer[]
        """
        for file in files:
            self.__gettersPool.put((file, force))

        self.__gettersPool.join()
        return self.__threads_dump_result()

    def del_files(self, files):
        """Delete files from storage

        :param files: file names at storage
        :type files: list
        :return: owl.Answer[]
        """
        r = []
        for file in files:
            r.append(self.__del_file(file))

        return r

    def __threads_get_file(self, i, q):
        """Thread wrapper for __get_file method

        :param i: number of thread
        :type i: int
        :param q: getters pool queue
        :type q: Queue
        """
        k = 0
        while True:
            k += 1
            try:
                item = q.get()
            except Empty as e:
                pass
            else:
                if item is not None:
                    if settings.DEBUG:
                        print('Thread {0} received item {1}'.format(i, item[0]))

                    self.__threads_result.append(self.__get_file(*item[0], force=item[1]))
                    q.task_done()

    def __threads_dump_result(self):
        """Dump threads result and clear stack

        :return: list
        """
        __tmp = self.__threads_result
        self.__threads_result = []
        return __tmp

    def __get_file(self, file, filters, force):
        """Get file from storage

        :param file: filename at storage
        :type file: tuple
        :param force: force cache ignore
        :type force: bool
        :return: owl.Answer
        """
        # Get file
        e = engines.get_engine(settings.STORAGE_ENGINE)
        e.client = self.__client

        return e.get_file(file, filters, force)

    def __del_file(self, file):
        """Delete file from storage

        :param file: filename at storage
        :type file: str
        :return: owl.Answer
        """
        # Get file
        e = engines.get_engine(settings.STORAGE_ENGINE)
        e.client = self.__client

        return e.del_file(file)
