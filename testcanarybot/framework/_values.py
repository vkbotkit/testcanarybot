from ..enums import values
from ..objects import expression

import typing
import random
import string


class expr(expression):
    def __init__(self, type: values, value: str):
        self.type = type
        self.value = value


def parsename(name: str):
    name = name.lower()
    test, i = len(name), 0

    while i< test:
        if name[i] not in [*string.ascii_lowercase, *string.digits]:
            name = name[:i] + name[i+1:]
            test -= 1

        else:
            i+= 1

    if name == '': name = 'module_' + gen_str()
    
    return name


def bool_str(line: str):
    if line.lower() in ['true', '1', 'правда', 'y', 'yes', 'да']:
        return True

    elif line.lower() in ['false', '1', 'ложь', 'n', 'no', 'нет']:
        return False

    else:
        raise ValueError("Wrong string")


def gen_str(test = None):
    result, num = "", random.randint(5, 25)

    if isinstance(test, int):
        num = test

    while num != 0:
        result += random.choice([
                *string.ascii_lowercase,
                *string.digits]
        )
        num -= 1
    return result


class global_expressions:
    def clear(self):
        self.__types = {
            values.workspace: [],
            values.log: [],
            values.tumbler: [],
            values.expr: [],
        }
        self.__values = {}

        self.set(name = "LOGGER_START", value = ":::LOGGER_START:::", type = values.log)
        self.set(name = "LOGGER_CLOSE", value = ":::LOGGER_END:::", type = values.log)
        
        self.set(name = "SESSION_START", value = "started", type = values.log)
        self.set(name = "SESSION_CLOSE", value = "closed", type = values.log)
        
        self.set(name = "LONGPOLL_START", value = "polling...", type = values.log)
        self.set(name = "LONGPOLL_CLOSE", value = "polling is finished", type = values.log)
        self.set(name = "LONGPOLL_CHECK", value = "polling...", type = values.log)
        self.set(name = "LONGPOLL_UPDATE", value = "server updated", type = values.log)
        self.set(name = "LONGPOLL_ERROR", value = "is not connected", type = values.log)

        self.set(name = "NO_THREAD", value = "launched with disabled threading", type = values.log)

        self.set(name = "LIBRARY_GET", value = "library directory is listed", type = values.log)
        self.set(name = "IMPORTERROR", value = "library directory is broken", type = values.log)

        self.set(name = "MODULE_INIT", value = "{module} is loaded", type = values.log)
        self.set(name = "MODULE_INIT_VOID", value = "\n\t\t + void", type = values.log)
        self.set(name = "MODULE_INIT_PRIORITY", value = "\n\t\t + {count} commands", type = values.log)
        self.set(name = "MODULE_INIT_EVENTS", value = "\n\t\t with {event}", type = values.log)
        self.set(name = "MODULE_INIT_ACTION", value = "\n\t\t with {action}", type = values.log)

        self.set(name = "UPLOADER_DEBUG", value = "appeared exception at {module}: {exception}", type = values.log)
        self.set(name = "API_DEBUG", value = "used method `{method}` with values {values}", type = values.log)

        self.set(name = "MODULE_FAILED_NOMAIN", value = "{module} loading failed: no 'Main' class", type = values.log)
        self.set(name = "MODULE_FAILED_HANDLERS", value = """{module} loading failed: no any handlers at module, write coroutine with these decorators:
            @objects.priority(commands = [], private = False)
            @objects.event(events = [], private = False)
            @objects.action(events = [], private = False)
            @objects.void
            
or create coroutine start(self, tools)""", type = values.log)
    
        self.set(name = "MODULE_ALREADY", value = "{module} loading failed: these {handler_type} already registered:\n{type_list}", type = values.log)
        self.set(name = "MODULE_ISALREADY", value = "{module} loading failed: {handler} is already registered", type = values.log)
        self.set(name = "MODULE_VALID", value = "{module} is valid, moving handlers into the main dictionary.", type = values.log)

        self.set(name = "MESSAGE_HANDLER_ITEMS", value = "\t\titems: {items}", type = values.log)
        self.set(name = "MESSAGE_HANDLER_TYPE", value = "{event_type}", type = values.log)
        self.set(name = "MESSAGE_HANDLER_CHAT", value = "\t\tpeer id: {peer_id}", type = values.log)
        self.set(name = "MESSAGE_HANDLER_USER", value = "\t\tfrom id: {from_id}", type = values.log)
        self.set(name = "MESSAGE_HANDLER_IT", value = "\t\ttext: {text}", type = values.log)

        self.set(name = "ENDLINE", type = values.workspace)
        self.set(name = "NOREPLY", type = values.workspace)

        self.set(name = "ALL_MESSAGES", value = False, type = values.tumbler)
        self.set(name = "ADD_MENTIONS", value = False, type = values.tumbler)
        self.set(name = "DEBUG_MESSAGES", value = False, type = values.tumbler)

        self.set(name = "LISTITEM", value = "\u2022", type = values.expr)
        self.set(name = "ADDITIONAL_MENTIONS", value = [], type = values.expr)


    def __getattr__(self, name: str):
        name = name.upper()
        if name in self.__values.keys():
            return self.__values[name]

        else:
            raise AttributeError(f"Unknown key: \"{name}\"")
    
    
    def type(self, name):
        for i in self.__types.keys():
            if name in self.__types[i]:
                return i
        raise NameError("\"{name}\" is not exists")
        

    def getKeys(self):
        return list(self.__values.keys())

    
    def set(self, name: str, value: typing.Optional[str] = None, type: typing.Optional[values] = None):
        name = name.upper()

        if not value and not isinstance(value, bool): 
            value = expr(type, name)

        if name not in self.__values.keys():
            if not type: 
                type = values.expr
            
            self.__types[type].append(name)
        elif type:
            for i in self.__types:
                if name in i and i != type:
                    pass
                else:
                    raise TypeError("Incorrect type for value:", type)
        self.__values[name] = value


    def switch(self, name: str, value: typing.Optional[bool] = None):
        name = name.upper()

        if name in self.__values[values.tumbler]: 
            if not isinstance(value, bool):
                value = not self.get(name)

            self.set(name = name, value = value)
            
        else:
            raise TypeError(f"\"{name}\" is not values.tumbler")

    
    __types: dict
    __values: dict
    __init__ = clear
    get = __getattr__



class _ohr:
    from_id = ['deleter_id', 'liker_id', 'user_id']
    peer_id = ['market_owner_id', 'owner_id', 'object_owner_id', 
                'post_owner_id', 'photo_owner_id', 'topic_owner_id', 
                'video_owner_id', 'to_id'
                ]
