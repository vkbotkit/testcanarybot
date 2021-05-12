from testcanarybot.packaet import log
from .data import *
from .decorators import *
from .tools import tools

import typing

class libraryModule:
    """
    Library Module object that contains handlers for events from chats
    """
    start: typing.Coroutine