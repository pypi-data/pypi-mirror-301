import logging
import colorlog

class Log:
    def __init__(self, name: str):
        self.log = logging.getLogger(name)
        self.log.setLevel(logging.DEBUG)

        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)

        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s | %(levelname)s | %(message)s",
            datefmt='%H:%M:%S',
            log_colors={
                '  DEBUG   ': 'cyan',
                '   INFO   ': 'green',
                ' WARNING  ': 'yellow',
                '  ERROR   ': 'red',
                ' CRITICAL ': 'bold_red',
            }
        )

        handler.setFormatter(formatter)
        self.log.addHandler(handler)

        self.center_log_levels()

    def center_log_levels(self):
        logging.addLevelName(logging.DEBUG, "  DEBUG   ")
        logging.addLevelName(logging.INFO, "   INFO   ")
        logging.addLevelName(logging.WARNING, " WARNING  ")
        logging.addLevelName(logging.ERROR, "  ERROR   ")
        logging.addLevelName(logging.CRITICAL, " CRITICAL ")

    def set_level(self, log_level: int):
        self.log.setLevel(log_level)
        for handler in self.log.handlers:
            handler.setLevel(log_level)

    def debug(self, msg, *args, **kwargs):
        self.log.debug(self._indent_message(msg), *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.log.info(self._indent_message(msg), *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.log.warning(self._indent_message(msg), *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.log.error(self._indent_message(msg), *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.log.critical(self._indent_message(msg), *args, **kwargs)

    def _indent_message(self, msg):
        return msg.replace('\n', '\n                        ')

log_instance = Log(__name__)

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

def level(log_level: int):
    log_instance.set_level(log_level)

def debug(msg, *args, **kwargs):
    log_instance.debug(msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    log_instance.info(msg, *args, **kwargs)

def warning(msg, *args, **kwargs):
    log_instance.warning(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    log_instance.error(msg, *args, **kwargs)

def critical(msg, *args, **kwargs):
    log_instance.critical(msg, *args, **kwargs)
