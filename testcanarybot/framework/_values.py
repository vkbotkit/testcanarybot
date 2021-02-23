from ..enums import values
from ..objects import expression

import typing
import random
import string


class expr(expression):
    def __init__(self, stype: values, value: typing.Optional[str] = None):
        self.type = stype
        self.value = value if value else None


def parsename(name: str):
    name = name.lower()
    test, i = len(name), 0
    while i< test:
        if name[i] not in [
                *string.ascii_lowercase,
                *string.digits]:
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
    __types = {
        values.workspace: [],
        values.log: [],
        values.expr: [],
        values.tumbler: [],
        values.hidden: ["BEEPA_PAPASA"]
    }
    __values = {}

    def __init__(self):
        self.__values["ALL_MESSAGES"] = expr(values.tumbler, False)
        self.__values["DEBUG_MESSAGES"] = expr(values.tumbler, False)
        self.__values["MENTIONS"] = expr(values.tumbler, False)

        self.__values["LOGGER_START"] = expr(values.log, """testcanarybot started here""")
        self.__values["LOGGER_CLOSE"] = expr(values.log, ["","$$$",""])

        self.__values["SESSION_START"] = expr(values.log, "started")
        self.__values["SESSION_CLOSE"] = expr(values.log, "closed")

        self.__values["LONGPOLL_START"] = expr(values.log, "polling is started \n")
        self.__values["LONGPOLL_CLOSE"] = expr(values.log, "polling is finished")
        self.__values["LONGPOLL_CHECK"] = expr(values.log, "checking...")
        self.__values["LONGPOLL_UPDATE"] = expr(values.log, "server updated")
        self.__values["LONGPOLL_ERROR"] = expr(values.log, "have not been connected")

        self.__values["LIBRARY_GET"] = expr(values.log, "library directory is listed")
        self.__values["LIBRARY_ERROR"] = expr(values.log, "library directory is broken")

        self.__values["MODULE_INIT"] = expr(values.log, "{module} is loaded")

        self.__values["MODULE_INIT"] = expr(values.log, "{module} is loaded")
        self.__values["MODULE_INIT_VOID"] = expr(values.log, "\n\t\t + void coroutine")
        self.__values["MODULE_INIT_PRIORITY"] = expr(values.log, "\n\t\t + registered {count} commands")
        self.__values["MODULE_INIT_EVENTS"] = expr(values.log, "\n\t\t with {event}")
        
        self.__values["MODULE_FAILED_BROKEN"] = expr(values.log, "{module} is broken: no 'Main' class")
        self.__values["MODULE_FAILED_VERSION"] = expr(values.log, "{module} is broken: unsupported version of that")
        self.__values["MODULE_FAILED_SUBCLASS"] = expr(values.log, "{module} is broken: is not inherited from testcanarybot.objects.libraryModule")
        self.__values["MODULE_FAILED_HANDLERS"] = expr(values.log, """{module} is broken: no any handlers at module, write coroutine with these decorators:
            @objects.libraryModule.priority(commands = [])
            @objects.libraryModule.event(events = [])
            @objects.libraryModule.void""")


        self.__values["MESSAGE_HANDLER_ITEMS"] = expr(values.log, "\t\titems: {items}")
        self.__values["MESSAGE_HANDLER_TYPE"] = expr(values.log, "{event_type}")
        self.__values["MESSAGE_HANDLER_CHAT"] = expr(values.log, "\t\tpeer id: {peer_id}")
        self.__values["MESSAGE_HANDLER_USER"] = expr(values.log, "\t\tfrom id: {from_id}")
        self.__values["MESSAGE_HANDLER_IT"] = expr(values.log, "\t\ttext: {text}")

        self.__values["ENDLINE"] = expr(values.workspace, ":::ENDLINE:::")
        self.__values["NOREPLY"] = expr(values.workspace, ":::NOREPLY:::")
        self.__values["TEST"] = expr(values.tumbler, ":::TEST:::")
        self.__values["BEEPA_PAPASA"] = expr(values.hidden, ":::NYASHKA:NYASHKA:::")
        self.__values["LISTITEM"] = expr(values.expr, "\u2022")


    def __getattr__(self, name: str):
        if name in self.__values.keys():
            return self.__values[name]
            
        return expr(values.empty, f":::{name}:UNKNOWN:::")

    @property
    def keys(self):
        return self.__values.keys()

    
    def set(self, name: str, value: typing.Any = None, stype: typing.Optional[values] = None):
        value = value if value else f":::{name}:::"
        stype = stype if stype else values.expr

        if name in self.__values.keys() and name not in self.__types[values.hidden]:
            self.__values[name].value = value

        else:
            if stype in self.__types.keys():
                self.__types[stype].append(name)
                self.__values[name] = expr(stype, value)

            else:
                raise TypeError("Incorrect exp_type")


class _ohr:
    from_id = ['deleter_id', 'liker_id', 'user_id']
    peer_id = ['market_owner_id', 'owner_id', 'object_owner_id', 
                'post_owner_id', 'photo_owner_id', 'topic_owner_id', 
                'video_owner_id', 'to_id'
                ]
