"""
Filter Module
~~~~~~~~~~~~~

The module implements the filter functionality of the Tea Logger.
"""

import logging


class StdoutFilter(logging.Filter):
    """Standard Output Filter"""

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter the specified record

        Determine if the specified record is to be logged.

        :param record: The record to filter
        :type record: dict

        :return: Whether or not the record should be logged
        :rtype: bool
        """

        # Log record(s) with a level of WARNING or lower
        return record.levelno <= logging.WARNING
