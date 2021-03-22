from .data import *
from .decorators import *
from .tools import tools


class libraryModule:
    codename = "testcanarybot_module"
    name = "testcanarybot sample module"
    description = "http://kensoi.github.io/testcanarybot/createmodule.html"

    void_react = False
    event_handlers = {}
    action_handlers = {}

    def __init__(self):
        self.commands = []
        self.handler_dict = {}
        self.void_react = False
        self.event_handlers = {} # event.abstract_event: []