import logging
from logging.handlers import RotatingFileHandler


class Logger:
    def __init__(self, name, log_file, level=logging.DEBUG, max_bytes=10000, backup_count=3):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        # Create handler with rotating file
        file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setLevel(level)
        # create formatter
        formatter = logging.Formatter('%(lineno)s - %(levelname)s: %(message)s (%(asctime)s)')
        file_handler.setFormatter(formatter)
        # add handler to logger
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger
