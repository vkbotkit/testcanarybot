import asyncio
from datetime import datetime
import importlib
import json
import os
import threading
import typing
import random

from .others.databases import databases
from .others import objects
from .others import exceptions
from .others.values import global_expressions, Pages
from .others.enums import events

class _assets:
    def __init__(self):
        self.path = os.getcwd() + '\\assets\\'

    def __call__(self, *args, **kwargs):
        args = list(args)
        if len(args) > 0:
            args[0] = self.path + args[0]
        
        elif 'file' in kwargs:
            kwargs['file'] = self.path + kwargs['file']
        
        return open(*args, **kwargs)

    def __exit__(self, exc_type, exc_value, traceback):
        pass

assets = _assets()
package_test = objects.package(**{'type': events.message_new, 'items': ['test']})



class library:
    modules = {}
    handlers = {
        'void': [], # [handler1, handler2]
        'priority': {}, # {'test', 'hello', 'world'}: [handler1, handler2, ...]
        'events': {} # event.abstract_event: [handler1, handler2]
    }

    def __init__(self, tools):
        self.tools = tools
        self.list = []
        self.void_react = False
        self.commands = []


    def getPriority(self, command):
        return self.handlers['priority'][command]

    def getVoid(self):
        return self.handlers['void']
            

    def upload(self, isReload = False, loop = asyncio.get_event_loop()):
        self.modules = {}

        if 'library' in os.listdir(os.getcwd()):
            self.tools.system_message(str(self.tools.values.LIBRARY_GET), module = "library.uploader")
            
            listdir = os.listdir(os.getcwd() + '\\library\\')
            if "__pycache__" in listdir: listdir.remove("__pycache__")
            if len(listdir) == 0:
                raise exceptions.LibraryError(
                    self.tools.values.SESSION_LIBRARY_ERROR)
            init_async(
                    asyncio.wait(
                        [
                            loop.create_task(self.upload_handler(module)) for module in listdir
                        ]
                    ), loop = loop
                )
            self.tools.system_message(
                "Supporting event types: {event_types}".format(
                    event_types = "\n".join(["", "\t\tevents.message_new", *["\t\t" + str(i) for i in self.handlers['events'].keys()], ""])
                ), module = "library.uploader", newline = True)
    

    async def upload_handler(self, module_name):
        module_name = "library." + (module_name[:-3] if module_name.endswith('.py') else module_name + '.main')
        module = importlib.import_module(module_name)

        if hasattr(module, 'Main'):
            moduleObj = module.Main()
            moduleObj.module_name = module_name
                    
            if not issubclass(type(moduleObj), objects.libraryModule):
                return self.tools.system_message(self.tools.values.MODULE_FAILED_SUBCLASS.value.format(
                    module = module_name), module = "library.uploader")

        else:
            return self.tools.system_message(self.tools.values.MODULE_FAILED_BROKEN.value.format(
                module = module_name), module = "library.uploader")
                
        for coro_name in set(dir(moduleObj)) - set(dir(objects.libraryModule)):
            coro = getattr(moduleObj, coro_name)

            if coro_name not in ['start', 'priority', 'void', 'event'] and callable(coro):
                try:
                    await coro(self.tools, package_test)

                except:
                    pass

        message = self.tools.values.MODULE_INIT.value.format(
            module = module_name)

        if len(moduleObj.commands) == 0 and len(moduleObj.event_handlers.keys()) == 0 and not moduleObj.void_react:
            return self.tools.system_message(self.tools.values.MODULE_FAILED_HANDLERS.value.format(
                module = module_name), module = "library.uploader")
        
        if len(moduleObj.commands) > 0:
            message += self.tools.values.MODULE_INIT_PRIORITY.value.format(count = len(moduleObj.commands))

            for i in moduleObj.handler_dict.values():
                for j in i['commands']:
                    if j not in self.handlers['priority']:
                        self.handlers['priority'][j] = []

                    self.handlers['priority'][j].append(i['handler'])

        if len(moduleObj.event_handlers.keys()) > 0:
            for event in moduleObj.event_handlers.keys():
                message += self.tools.values.MODULE_INIT_EVENTS.value.format(event = str(event))
                if not event in self.handlers['events']:
                    self.handlers['events'][event] = []

                self.handlers['events'][event].extend(moduleObj.event_handlers[event])
        

        if moduleObj.void_react:
            self.handlers['void'].append(moduleObj.void_react)
            self.void_react = True
            message += self.tools.values.MODULE_INIT_VOID.value

        self.modules[module_name] = moduleObj
        self.list = module_name
        return self.tools.system_message(write = message, module = "library.uploader")


class tools():
    __module = "system_message"
    __db = databases(("system", "system.db"))
    mentions = list()
    mentions_name_cases = []

    group_id = 0
    name_cases = [
            'nom', 'gen', 
            'dat', 'acc', 
            'ins', 'abl'
            ]

    mentions_self = {
        'nom': 'я', 
        'gen': ['меня', 'себя'],
        'dat': ['мне', 'себе'],
        'acc': ['меня', 'себя'],
        'ins': ['мной', 'собой'],
        'abl': ['мне','себе'],
    }
    mentions_unknown = {
        'all': 'всех',
        'him': 'его',
        'her': 'её',
        'it': 'это',
        'they': 'их',
        'them': 'их',
        'us': 'нас',
        'everyone': ['@everyone', '@all', '@все']
    }

    def __init__(self, group_id, api, http, log):
        self.values = global_expressions()
        self.group_id = group_id
        self.api = api
        self.assets = assets
        self.http = http
        self.log = log
        self.waiting_replies = {}
        
        init_async(self.__setShort())

        self.group_mention = f'[club{self.group_id}|@{self.group_address}]'
        self.mentions = [self.group_mention]

        self.get = self.__db.get
        threading.current_thread()

    
    def random_id(self) -> int:
        return random.randint(0, 99999999)

    
    def ischecktype(self, checklist, checktype) -> bool:
        for i in checklist:
            if isinstance(checktype, list) and type(i) in checktype:
                return True
                
            elif isinstance(checktype, type) and isinstance(i, checktype): 
                return True
            
        return False
    
    
    def parse_mention(self, ment) -> objects.mention:
        page_id, call = ment[0: ment.find('|')], ment[ment.find('|') + 1:]

        page_id = page_id.replace('id', '')
        page_id = page_id.replace('club', '-')
        page_id = page_id.replace('public', '-')
            
        return objects.mention(int(page_id), call)


    def parse_link(self, link) -> str:
        response = link

        response.replace('https://', '')
        response.replace('http://', '')
        
        return response


    def getDate(self, time = None) -> str:
        if not time: time = datetime.now()
        return f'{"%02d" % time.day}.{"%02d" % time.month}.{time.year}'
    
    
    def getTime(self, time = None) -> str:
        if not time: time = datetime.now()
        return f'{"%02d" % time.hour}:{"%02d" % time.minute}:{"%02d" % time.second}.{time.microsecond}'


    def getDateTime(self, time = None) -> str:
        if not time: time = datetime.now()
        return self.getDate(time) + ' ' + self.getTime(time)


    async def __setShort(self):
        res = await self.api.groups.getById(group_id=self.group_id)
        self.group_address = res[0].screen_name
        return
    

    async def wait_reply(self, package):
        wait = objects.WaitReply(package)
        self.waiting_replies[wait] = False

        while True:
            if self.waiting_replies[wait]: 
                return self.waiting_replies.pop(wait)
            
            await asyncio.sleep(0)


    def system_message(self, *args, write = None, module = None, newline = False):
        if not module: module = self.__module
        if not write: write = " ".join([str(i) for i in list(args)])
        
        response = f'@{self.group_address}.{module}: {write}'

        if self.log.closed:
            self.log = assets("log.txt", "a+", encoding="utf-8")

        newline_res = "\n" if newline else ""
        print(newline_res + response)

        response = f'{self.getDateTime()} {response}'
        print(newline_res + response, file=self.log)

        self.log.flush()

    
    def makepages(self, obj:list, page_lenght: int = 5, listitem: bool = False):
        listitem_symb = self.values.LISTITEM if listitem else str()
        return Pages(obj, page_lenght, listitem_symb)


    def add(self, db_name):
        self.__db.add((db_name, self.assets.path + db_name))


    async def getMention(self, page_id: int, name_case = "nom"):
        if name_case == 'link':
            if page_id > 0:
                return f'[id{page_id}|@id{page_id}]'

            elif page_id == self.group_id:
                return self.group_mention

            else:
                test = await self.api.groups.getById(group_id = -page_id)
                return f'[club{-page_id}|@{test[0].screen_name}]'
        
        else:
            if page_id > 0:
                request = await self.api.users.get(
                    user_ids = page_id, 
                    name_case = name_case
                    )
                first_name = request[0].first_name
                
                return f'[id{page_id}|{first_name}]'
            
            elif page_id == self.group_id:
                return self.mentions_self[name_case]
            
            else:
                request = await self.api.groups.getById(
                    group_id = -page_id
                    )
                name = request[0].name
                
                return f'[club{-page_id}|{name}]' 


    async def getManagers(self, group_id = None):
        if not group_id:
            group_id = self.group_id

        elif not isinstance(group_id, int):
            raise TypeError('Group ID should be integer')

        lis = await self.api.groups.getMembers(group_id = group_id, sort = 'id_asc', filter='managers')
        return [i.id for i in lis.items if i.role in ['administrator', 'creator', 'moderator']]


    async def isManager(self, from_id: int, group_id = None):
        if not group_id:
            group_id = self.group_id
            
        elif not isinstance(group_id, int):
            raise TypeError('Group ID should be integer')

        return from_id in await self.getManagers(group_id)


    async def getChatManagers(self, peer_id: int):
        res = await self.api.messages.getConversationsById(peer_ids = peer_id)
        res = res.items[0].chat_settings
        response = [*res.admin_ids, res.owner_id]
        return response
        

    def isChatManager(self, from_id, peer_id: int):
        return from_id in self.getChatManagers(peer_id)


    async def getMembers(self, peer_id: int):
        response = await self.api.messages.getConversationMembers(peer_id = peer_id)
        return [i['member_id'] for i in response['items']]


    async def isMember(self, from_id: int, peer_id: int):
        return from_id in await self.getMembers(peer_id)


def init_async(coro: asyncio.coroutine, loop = asyncio.get_event_loop()):
    if loop.is_running():
        raise exceptions.LoopStateError("This event loop is currently running")

    else:
        return loop.run_until_complete(coro)
