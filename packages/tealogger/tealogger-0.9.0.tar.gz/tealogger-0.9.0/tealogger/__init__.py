"""
Tea Logger Package
~~~~~~~~~~~~~~~~~~

Tea Logger is a simple logging package for Python.
"""

# Class
from .tealogger import TeaLogger

# Level
from .tealogger import DEBUG
from .tealogger import INFO
from .tealogger import WARNING
from .tealogger import ERROR
from .tealogger import CRITICAL
from .tealogger import NOTSET

# Function
from .tealogger import configure
from .tealogger import get_logger
from .tealogger import getLogger
from .tealogger import set_level
from .tealogger import setLevel
from .tealogger import log
from .tealogger import debug
from .tealogger import info
from .tealogger import warning
from .tealogger import error
from .tealogger import critical

__all__ = [
    # Class
    'TeaLogger',

    # Level
    'DEBUG',
    'INFO',
    'WARNING',
    'ERROR',
    'CRITICAL',
    'NOTSET',

    # Function
    'configure',
    'get_logger',
    'getLogger',
    'set_level',
    'setLevel',
    'log',
    'debug',
    'info',
    'warning',
    'error',
    'critical'
]
