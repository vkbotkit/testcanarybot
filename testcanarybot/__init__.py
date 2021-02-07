from .source.application import app
from .source.library import init_async
from .source.versions import current

__all__ = ['enums', 'exceptions', 'objects', 'tools']
__version__ = current

__title__ = 'TestCanaryBot, ' + current
__author__ = 'Kensoi'
__license__ = 'Apache v2'
__copyright__ = 'Copyright 2020 by Kensoi'

__doc__ = "kensoi/testcanarybot, " + current + """
Documentation is available at kensoi.github.io/testcanarybot
"""