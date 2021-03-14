from datetime import datetime
from .enums import values as __values

import abc
import random
import typing


class expression:
    __slots__ = ('type', 'value')

    def __init__(self):
        self.type = None
        self.value = None

    def __str__(self):
        return self.value

    def __int__(self):
        return self.value
    
    def __list__(self):
        return self.value


class mention:
    __slots__ = ('id', 'call') 
    def __init__(self, page_id, mention = ""):
        self.id = page_id
        self.call = mention

    def __int__(self):
        return self.id 

    def __str__(self):
        return self.call    
        

class data:
    def __init__(self, entries):
        self.__dict__.update(entries)

        for i in self.__dict__.keys():
            setattr(self, i, self.__convert(getattr(self, i)))

        self.raw = entries
            

    def __convert(self, attr):
        attr_type = type(attr)

        if attr_type == dict:
            return key(attr)

        elif attr_type == list:
            return [self.__convert(i) for i in attr]
        
        else:
            return attr  

    def __repr__(self):
        return '<{}({})>'.format(type(self), self.raw)
  


class key(data):
    pass


class package(data):
    __item = "$item"
    __items = "$items"
    __mention = "$mention"
    __mentions = "$mentions"
    __expr = "$expr"
    __exprs = "$exprs"

    id = 0
    date = 0
    random_id = 0
    peer_id = 1
    from_id = 1
    items = []
                

    class params:
        action = False
        attachments = False
        payload = False
        command = False
        from_chat = False
        gment = ""
        mentions = []
        key_start = 0


    type = ''


    def getItems(self):
        return self.items[:-1]
            

    def check(self, command: list) -> typing.Union[bool, list]:
        """
        Following keys:
        $item - any string
        $items - any string
        $expr - expression item
        $exprs - list from this item to the end is a list of expression objects
        $mention - mention item
        $mentions - list from this item to the end is a list of mention objects
        """
        if len(self.items) == 0:
            return False
        
        if command[-1] not in [self.__mentions, self.__exprs, self.__items]:
            if len(command) + 1 != len(self.items): 
                return False

        for i in range(len(command)):
            if command[i] == self.items[i]:
                continue
                
            elif command[i] == self.__item:
                if not isinstance(self.items[i], str):
                    return False
                continue

            elif command[i] == self.__items:
                return self.items[i:-1]

            elif command[i] == self.__expr:
                if not isinstance(self.items[i], (expression, str)):
                    return False
                continue

            elif command[i] == self.__mention:
                if not isinstance(self.items[i], mention):
                    return False
                continue

            elif command[i] == self.__exprs:
                if not isinstance(j, expression):
                    return False
                return self.items[i:-1]

            elif command[i] == self.__mentions:
                mentions = 0
                for j in self.items[i:-1]:
                    if not isinstance(j, (mention, str)):
                        return False
                    mentions += 1

                if mentions > 1:
                    return self.items[i:-1]
                else:
                    return False

            else:
                return False
            
        return True


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


def ContextManager(
        events: typing.Optional[list] = None, 
        commands: typing.Optional[list] = None, 
        action: typing.Optional[list] = None, 
        # payload: typing.Optional[list] = None
        ):

    def decorator(coro: typing.Callable):
        def registerCommand(self):
            if events:
                from .enums import events as enums_events
                for i in events:
                    if not isinstance(i, enums_events):
                        raise TypeError("Incorrect type!")

                    elif i not in self.event_handlers and i != enums_events.message_new:
                        self.event_handlers[i] = coro
                    else:
                        raise exceptions.LibraryRewriteError(f"{str(i)} is already registered event")
                
                return # coro(self, *args, **kwargs) 

            if commands:
                self.commands.extend(commands)
                self.handler_dict[coro.__name__] = {'handler': coro, 'commands': commands}

                return # coro(self, *args, **kwargs)

            if action:
                from .enums import action as enums_action
                for i in action:
                    if not isinstance(i, enums_action):
                        raise TypeError("use testcanarybot.enums.action for this context!")
                    
                    if i not in self.action_handlers:
                        self.action_handlers[i] = coro
                    
                    else:
                        raise exceptions.LibraryRewriteError(f"{str(i)} is already registered action")


                return # coro(self, *args, **kwargs)

            if not (events or commands or action):
                if self.void_react:
                    raise NameError("Void handler is already created")

                self.void_react = coro
                return # coro(self, *args, **kwargs)
        
        return registerCommand
    return decorator


def event(events: list):
    return ContextManager(events = events)


def priority(commands: list):
    return ContextManager(commands = commands)


def void(coro: typing.Callable):
    return ContextManager()(coro)
    

def action(action: list()):
    return ContextManager(action = action)


class tools(abc.ABCMeta):
    __module = "system"
    
    @property
    @abc.abstractmethod
    def name_cases(self):
        pass

    @property
    @abc.abstractmethod
    def mentions_self(self):
        pass

    @property
    @abc.abstractmethod
    def mentions_unknown(self):
        pass

    @property
    @abc.abstractmethod
    def values(self):
        return self.__values

    @property
    @abc.abstractmethod
    def link(self):
        pass

    @property
    @abc.abstractmethod
    def mention(self):
        pass

    @property
    @abc.abstractmethod
    def mentions(self):
        pass

    @property
    @abc.abstractmethod
    def api(self):
        pass

    @property
    @abc.abstractmethod
    def groupId(self):
        pass
        
    @property
    @abc.abstractmethod
    def http(self):
        pass
        
    @property
    @abc.abstractmethod
    def log(self):
        pass

    @property
    @abc.abstractmethod
    def random_id(self):
        pass


    @abc.abstractmethod
    def system_message(self, *args, write = None, module = None, newline = False) -> None:
        pass


    @abc.abstractmethod
    def getDate(self, time = None) -> str:
        pass
    
    
    @abc.abstractmethod
    def getTime(self, time = None) -> str:
        pass


    @abc.abstractmethod
    def getDateTime(self, time = None) -> str:
        pass
    

    @abc.abstractmethod
    def ischecktype(self, checklist, checktype) -> bool:
        pass


    @abc.abstractmethod
    def wait_check(self, package) -> bool:
        pass


    @abc.abstractmethod
    async def wait_reply(self, package: package) -> package:
        pass


    @abc.abstractmethod
    async def getMention(self, page_id: int, name_case = "nom") -> str:
        pass


    @abc.abstractmethod
    async def getManagers(self, group_id = None) -> list:
        pass


    @abc.abstractmethod
    async def isManager(self, from_id: int, group_id = None) -> bool:
        pass


    @abc.abstractmethod
    async def getChatManagers(self, peer_id: int) -> list:
        pass
        

    @abc.abstractmethod
    def isChatManager(self, from_id, peer_id: int) -> bool:
        pass


    @abc.abstractmethod
    async def getMembers(self, peer_id: int):
        pass


    @abc.abstractmethod
    async def isMember(self, from_id: int, peer_id: int) -> bool:
        pass


