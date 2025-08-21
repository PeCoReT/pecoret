import os
from logging.handlers import RotatingFileHandler as LogRotatingFileHandler


class RotatingFileHandler(LogRotatingFileHandler):
    def __init__(self, filename, *args, **kwargs):
        self.make_directory(os.path.dirname(filename))
        super().__init__(filename, *args, **kwargs)

    @staticmethod
    def make_directory(path):
        os.makedirs(path, exist_ok=True)
