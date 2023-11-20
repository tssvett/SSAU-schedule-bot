import logging
import sys
import os


class LevelChooseException(Exception):
    """
    Specific exception class for wrong level
    """
    def __init__(self, message):
        self.message = message


class Logger:
    """
    Logger class. Output message to console and {Logger.name}.log file inside Logs directory.

    Allowed levels for use: 'info', 'error', 'debug', 'exception'

    Use the same names for loggers if you need to store information in one file (with the name of the logger)

    Use different names for loggers if you need to store information separately from each other (in different files)

    """
    def __init__(self, name: str):
        self._name = name
        self._log_path = self._create_logs_path()
        self._allowed_levels = ['info', 'error', 'debug', 'exception']
        self._log_core = logging.getLogger(name)
        self._log_core.setLevel(level=logging.DEBUG)
        self._file_handler = logging.FileHandler(self._log_path)
        self._console_handler = logging.StreamHandler(stream=sys.stdout)
        self._set_format()
        self._add_all_handlers()

    def send_message(self, message: str, level: str) -> None:
        """
        Sends message to console and log file in Logs directory.
        :param: message: String information message
        :param: level: 'info', 'error', 'debug' , 'exception'
        :return: None
        """
        if level == 'info':
            self._log_core.info(message)
        elif level == 'error':
            self._log_core.error(message)
        elif level == 'debug':
            self._log_core.debug(message)
        elif level == 'exception':
            self._log_core.exception(message)
        else:
            raise LevelChooseException("Invalid output level! Please use 'info', 'error', 'debug' or 'exception'")

    def get_log_path(self) -> os.path:
        """
        Returns path to this logger path file
        :return: String path
        """
        return self._log_path

    def get_allowed_levels(self) -> list:
        """
        Returns list of allowed levels
        :return: List of allowed levels
        """
        return self._allowed_levels

    def _create_logs_path(self) -> os.path:
        """
        Creates path to log file (create Logs directory higher in the directory tree if not exists).
        :return: Path to log file
        """
        log_path = os.path.join(os.path.dirname(__file__)[:-4], 'Logs', f'{self._name}.log')
        if not os.path.exists(os.path.dirname(log_path)):
            os.makedirs(os.path.dirname(log_path))
        return log_path

    def _add_all_handlers(self) -> None:
        """
        Apply all handlers to logger.
        :return: None
        """
        self._log_core.addHandler(self._file_handler)
        self._log_core.addHandler(self._console_handler)

    def _set_format(self) -> None:
        """
        Sets logging format.
        :return: None
        """
        for_file = '[%(asctime)s: %(levelname)s %(message)s]'
        for_console = '[%(asctime)s: %(levelname)s %(message)s]'
        file_format = logging.Formatter(fmt=for_file)
        console_format = logging.Formatter(fmt=for_console)
        self._file_handler.setFormatter(file_format)
        self._console_handler.setFormatter(console_format)
