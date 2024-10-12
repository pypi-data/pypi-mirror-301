"""
Formatter Module
~~~~~~~~~~~~~~~~

The module implements the formatter functionality of the Tea Logger.
"""

import logging
from typing import Union


ESC = '\x1b['

_COLOR_CODE = {
    # Reset
    'RESET': f'{ESC}0m',
    # Foreground
    'FOREGROUND_BLACK': f'{ESC}30m',
    'FOREGROUND_RED': f'{ESC}31m',
    'FOREGROUND_GREEN': f'{ESC}32m',
    'FOREGROUND_YELLOW': f'{ESC}33m',
    'FOREGROUND_BLUE': f'{ESC}34m',
    'FOREGROUND_MAGENTA': f'{ESC}35m',
    'FOREGROUND_CYAN': f'{ESC}36m',
    'FOREGROUND_WHITE': f'{ESC}37m',
    'FOREGROUND_DEFAULT': f'{ESC}39m',
    # Background
    'BACKGROUND_BLACK': f'{ESC}40m',
    'BACKGROUND_RED': f'{ESC}41m',
    'BACKGROUND_GREEN': f'{ESC}42m',
    'BACKGROUND_YELLOW': f'{ESC}43m',
    'BACKGROUND_BLUE': f'{ESC}44m',
    'BACKGROUND_MAGENTA': f'{ESC}45m',
    'BACKGROUND_CYAN': f'{ESC}46m',
    'BACKGROUND_WHITE': f'{ESC}47m',
    'BACKGROUND_DEFAULT': f'{ESC}49m',
    # Style
    'STYLE_BOLD': f'{ESC}1m',
    'STYLE_DIM': f'{ESC}2m',
    'STYLE_UNDERLINED': f'{ESC}4m',
    'STYLE_BLINK': f'{ESC}5m',
    'STYLE_REVERSE': f'{ESC}7m',
    'STYLE_HIDDEN': f'{ESC}8m',
    'STYLE_DEFAULT': f'{ESC}22m',
}

_LEVEL_COLOR_CODE = {
    'NOTSET': _COLOR_CODE['RESET'],
    'DEBUG': _COLOR_CODE['FOREGROUND_CYAN'],
    'INFO': _COLOR_CODE['FOREGROUND_GREEN'],
    'WARNING': _COLOR_CODE['FOREGROUND_YELLOW'],
    'SUCCESS': _COLOR_CODE['FOREGROUND_GREEN'],
    'ERROR': _COLOR_CODE['FOREGROUND_RED'],
    'CRITICAL': f"{_COLOR_CODE['FOREGROUND_RED']}{_COLOR_CODE['BACKGROUND_WHITE']}",
}

class ColorFormatter(logging.Formatter):
    """Color Formatter

    Define a color Formatter.
    """

    def __init__(
        self,
        record_format: Union[str, None] = None,
        date_format: Union[str, None] = None
    ) -> None:
        """Initialize Constructor

        :param record_format: The record format for the Formatter,
            defaults to None, set from configuration
        :type record_format: str, optional
        :param date_format: The date format for the Formatter, defaults
            to None, set from configuration
        :type date_format: str, optional
        """

        # Call super class
        super().__init__(fmt=record_format, datefmt=date_format)

        self._level_format = {
            logging.DEBUG: (
                f"{_LEVEL_COLOR_CODE['DEBUG']}"
                f"{record_format}"
                f"{_LEVEL_COLOR_CODE['NOTSET']}"
            ),
            logging.INFO: (
                f"{_LEVEL_COLOR_CODE['INFO']}"
                f"{record_format}"
                f"{_LEVEL_COLOR_CODE['NOTSET']}"
            ),
            logging.WARNING: (
                f"{_LEVEL_COLOR_CODE['WARNING']}"
                f"{record_format}"
                f"{_LEVEL_COLOR_CODE['NOTSET']}"
            ),
            logging.ERROR: (
                f"{_LEVEL_COLOR_CODE['ERROR']}"
                f"{record_format}"
                f"{_LEVEL_COLOR_CODE['NOTSET']}"
            ),
            logging.CRITICAL: (
                f"{_LEVEL_COLOR_CODE['CRITICAL']}"
                f"{record_format}"
                f"{_LEVEL_COLOR_CODE['NOTSET']}"
            ),
        }

        self._date_format = date_format

    def format(
        self,
        record: logging.LogRecord
    ) -> str:
        """Format the specified record as text (redefined)

        :param record: The record to format, used for string formatting
            operation
        :type record: dict

        :return: The formatted record
        :rtype: str
        """
        log_format = self._level_format.get(record.levelno)
        formatter = logging.Formatter(
            fmt=log_format,
            datefmt=self._date_format
        )

        return formatter.format(record)
