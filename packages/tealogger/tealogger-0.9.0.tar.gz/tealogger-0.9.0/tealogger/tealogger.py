"""
Tea Logger Module
~~~~~~~~~~~~~~~~~

The module implements the core functionality of the Tea Logger.
"""

import json
import logging
import logging.config
from os import PathLike
from pathlib import Path
from typing import Union


# Log Level
CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET


# Default
DEFAULT_CONFIGURATION = None
CURRENT_MODULE_PATH = Path(__file__).parent.expanduser().resolve()
with open(
    CURRENT_MODULE_PATH / 'configuration' / 'default.json',
    mode='r',
    encoding='utf-8'
) as file:
    DEFAULT_CONFIGURATION = json.load(file)


class TeaLogger(logging.Logger):
    """Tea Logger"""

    def __new__(
        cls,
        name: Union[str, None] = None,
        level: Union[int, str] = NOTSET,
        **kwargs
    ):
        """Create Constructor

        Create new instance of the TeaLogger class.

        :param name: The name for the TeaLogger, defaults to None
        :type name: str or None, optional
        :param level: The level for the TeaLogger, defaults to NOTSET
        :type level: int or str, optional
        :param dictConfig: The dictionary configuration for the
            TeaLogger, defaults to None
        :type dictConfig: dict, optional
        :param fileConfig: The file configuration for the TeaLogger,
            defaults to None
        :type fileConfig: str, optional

        :return: The new instance of TeaLogger class (Self)
        :rtype: TeaLogger
        """

        # Configuration
        if kwargs.get('dictConfig'):
            # NOTE: No Coverage
            # Dictionary
            # configuration = kwargs.get('dictConfig')

            # if 'loggers' not in configuration:
            #     configuration['loggers'] = {}
            #     configuration['loggers'][name] = {
            #         'propagate': kwargs.get('propagate', False),
            #         'handlers': kwargs.get('handler_list', ['default'])
            #     }

            logging.config.dictConfig(kwargs.get('dictConfig'))
        elif kwargs.get('fileConfig'):
            # File
            ...
        else:
            # Default
            if 'loggers' not in DEFAULT_CONFIGURATION:
                DEFAULT_CONFIGURATION['loggers'] = {}
            if name not in DEFAULT_CONFIGURATION['loggers']:
                # Configure new logger with default configuration
                DEFAULT_CONFIGURATION['loggers'][name] = {
                    'propagate': kwargs.get('propagate', False),
                    'handlers': kwargs.get('handler_list', ['default'])
                }

                # configuration['loggers'][name]['handlers'] = kwargs.get('handler_list')

                # NOTE: Override only individual configuration!
                # Overriding the entire configuration will cause this child
                # logger to inherit any missing configuration from the root
                # logger. (Even if the configuration was set previously.)
                DEFAULT_CONFIGURATION['loggers'][name]['level'] = logging.getLevelName(level)
                # configuration['loggers'][name]['level'] = level

            logging.config.dictConfig(DEFAULT_CONFIGURATION)

        # Get (Create) the Logger
        tea = logging.getLogger(name)

        return tea

    def __init__(
        self,
        name: str,
        level: Union[int, str] = NOTSET
    ) -> None:
        """Initialize Constructor

        Initialize the instance of the TeaLogger class.

        :param name: The name for the TeaLogger
        :type name: str
        :param level: The level for the TeaLogger, defaults to NOTSET
        :type level: int or str, optional
        :return: The new instance of TeaLogger class (Self)
        :rtype: TeaLogger
        """
        # Call super class
        super().__init__(self, name=name, level=level)
        # logging.Logger.__init__(self, name=name, level=level)


tea = TeaLogger(
    name=__name__,
    level=WARNING,
)


def configure(configuration: dict | PathLike):
    """Configure the Tea Logger with the given configuration.

    :param configuration: The configuration for the Tea Logger
    :type configuration: dict or PathLike
    """
    if not isinstance(configuration, dict):
        try:
            with open(
                configuration,
                mode='r',
                encoding='utf-8'
            ) as file:
                configuration = json.load(file)
        except Exception:
            raise

    logging.config.dictConfig(configuration)


def get_logger(
    name: str,
):
    """Get the configured Tea Logger instance.

    :param name: The name for the configured TeaLogger
    :type name: str

    :return: The configured Tea Logger instance
    :rtype: TeaLogger
    """
    return logging.getLogger(name)


# Alias
getLogger = get_logger


def set_level(
    level: Union[int, str] = NOTSET,
):
    """Set the logging level of the Tea Logger (Package).

    :param level: The level for the TeaLogger, defaults to NOTSET
    :type level: int or str, optional
    """
    tea.setLevel(level)


# Alias
setLevel = set_level


def log(
    level: Union[int, str],
    message: str,
    *args,
    **kwargs
):
    """Log message with give level severity.

    :param level: The severity level for the log
    :type level: int, use predefined log level
    :param message: The message to log
    :type message: str
    """

    if isinstance(level, str):
        level = logging.getLevelName(level)

    tea.log(
        level=level,
        msg=message,
        *args,
        **kwargs
    )


def debug(
    message: str,
    *args,
    **kwargs
):
    """Log message with severity DEBUG level.

    :param message: The message to log
    :type message: str
    """
    tea.debug(message, *args, **kwargs)


def info(
    message: str,
    *args,
    **kwargs
):
    """Log message with severity INFO level.

    :param message: The message to log
    :type message: str
    """
    tea.info(message, *args, **kwargs)


def warning(
    message: str,
    *args,
    **kwargs
):
    """Log message with severity WARNING level.

    :param message: The message to log
    :type message: str
    """
    tea.warning(message, *args, **kwargs)


def error(
    message: str,
    *args,
    **kwargs
):
    """Log message with severity ERROR level.

    :param message: The message to log
    :type message: str
    """
    tea.error(message, *args, **kwargs)


def critical(
    message: str,
    *args,
    **kwargs
):
    """Log message with severity CRITICAL level.

    :param message: The message to log
    :type message: str
    """
    tea.critical(message, *args, **kwargs)
