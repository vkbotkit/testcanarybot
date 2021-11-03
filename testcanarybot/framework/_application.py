from .. import exceptions
from .. import objects
from ..enums import events

from ._api import api
from ._threading import (thread as handlering_thread, packageHandler as handler)
from ._library import library as _library
from ._values import global_expressions

import logging
import asyncio
import aiohttp
import atexit
import os
import threading
import time
import typing
import random


logger_levels = {
    'CRITICAL': 50,
    'ERROR': 40,
    'WARNING': 30,
    'INFO': 20,
    'DEBUG': 10,
    'NOTSET': 0
}


class _assets:
    def __init__(self, assets = os.getcwd() + '\\assets'):
        self.__path = assets + '\\'


    def __call__(self, *args, **kwargs):
        args = list(args)

        if len(args) > 0:
            args[0] = self.__path + args[0]
        
        elif 'file' in kwargs:
            kwargs['file'] = self.__path + kwargs['file']
        
        return open(*args, **kwargs)


    def __exit__(self, exc_type, exc_value, traceback):
        pass


class async_sessions():
    """
    wrapper over about aiohttp.request() to avoid errors about loops in threads
    headers: dict()
    """

    def __init__(self, *args, **kwargs):
        self.__args = args
        self.__kwargs = kwargs
        self.__sessions = []


    def create_session(self, thread: threading.Thread) -> None:
        if not hasattr(thread, 'session'): 
            thread.session = aiohttp.ClientSession(*self.__args, **self.__kwargs)
            self.__sessions.append(thread.session)


    def __del__(self):
        for session in self.__sessions:
            asyncio.get_event_loop().run_until_complete(session.close())
        

    def __getattr__(self, name):
        if name in dir(aiohttp.ClientSession):
            thread = threading.current_thread()
            self.create_session(thread)
            return getattr(thread.session, name)


class _app:  
    _headers = {'User-agent': """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"""}
    __longpoll_url = ""
    __longpoll_ts = 0
    __longpoll_key = None
    __booted_once = False


    def __init__(self, accessToken: str, groupId: typing.Union[str, int], apiVersion: str = "5.126", serviceToken: str = "", 
                    logg = logging.Logger(name = "testcanarybot"), level: str = 'info', 
                    print_log: bool = False, path = os.getcwd(), countThread: int = 0, assets = 'assets', library = 'library'):
        """
        testcanarybot project core (application)

        # VK Bots API
        accessToken     [str]                       community access token
        groupId         [str, int]                  community identificator
        apiVersion      [str: "5.130"]              set API version for your bot.
        serviceToken    [str]                       token for service access

        # Logger
        logg            [object: logging.Logger()]  your logger
        level           [str, int: "info"]          logging level [CRITICAL/ERROR/WARNING/INFO/DEBUG/NOTSET]

        # Core settings
        print_log       [bool: False]               print log to console
        path            [str: os.getcwd()]          project path
        countThread     [int: 1]                    set threads count for handlers.
        assets          [str: "assets"]             current assets directory name (only name without path)
        library         [str: "library"]            current library directory name (only name without path)
        """
        self.__thread = []
        self.__access = accessToken
        self.__service = serviceToken
        self.__group_id = int(groupId)
        self.__countThread = countThread
        self.__lastthread = 0
        self.__av = apiVersion
        self.__longpoll_delay = 1 / 20
        self.__longpoll_last = 0.0  
        self.__http = async_sessions(headers = self._headers, trust_env=True)
        self.__api = api(self.__http, self.method)
        self.logger = logg

        if isinstance(level, str):
            level = level.upper()
            level = logger_levels[level]

        self.logger.setLevel(level)
        handlerfile = logging.FileHandler("log.txt")
        self.logger.addHandler(handlerfile)

        if threading.current_thread() == threading.main_thread():
            self.__loop = asyncio.get_event_loop()
            
        else:
            self.__loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.__loop)


        self.__tools = tools(self.__group_id, self.__api, self.__http, os.getcwd() + '\\' + assets, self.logger, level, print_log)
        self.__tools.system_message(module = "session", level = "info", write = self.tools.values.SESSION_START)
            
        self.__library = _library(self.tools, library)
        atexit.register(self.__close)


    @property
    def countThread(self):
        return self.__countThread


    @property
    def http(self):
        return self.__http


    @property
    def log(self):
        return self.logger.handlers[0].baseFilename


    @property
    def tools(self):
        return self.__tools


    @property
    def api(self):
        return self.__api


    @property
    def api_url(self):
        return "https://api.vk.com/method/"


    def __close(self):
        self.__tools.system_message(module = "session", level = "info", write = self.__tools.values.SESSION_CLOSE)
        

    async def method(self, method: str, data: dict = {}):
        """ 
        raw API call

        method [str] - method name
        data [dict: {}] - parameters.
        """

        delay = self.__longpoll_delay - (time.time() - self.__longpoll_last)

        if 'group_id' in data: data['group_id'] = self.__group_id
        data['v'] = self.__av

        if 'type' in data:
            if data['type'] == 'service':
                data['access_token'] = self.__service
            
            else:
                data['access_token'] = self.__access
            
            del data['type']
        
        else:
            data['access_token'] = self.__access

        if delay > 0: await asyncio.sleep(delay)

        response = await self.http.post(self.api_url + method, data = data)
        response = await response.json()

        self.last_request = time.time()

        if 'error' in response: 
            raise exceptions.MethodError(f"[{response['error']['error_code']}] {response['error']['error_msg']}")

        return response['response']     


    def setMentions(self, mentions: list):
        """
        Setup custom mentions instead "@{group_address}"
        """
        resource = []
        resource.append(self.tools._tools__group_mention)
        mentions = map(str, mentions)
        mentions = map(lambda value: value.lower(), mentions)
        mentions = list(mentions)

        self.tools._tools__mentions = mentions  


    def setup(self):  
        """
        [Optional] Install components to work with longpoll and your handlers.
        """  
          
        self.__library.upload()

        self.logger.info(self.tools.values.LOGGER_START)
        if self.__countThread > 0:
            if len(self.__thread) <= self.__countThread:
                current_thread = threading.currentThread()

                for i in range(self.countThread):
                    thread_started = handlering_thread(self.__library, i, current_thread.getName())
                    
                    self.__thread.append(thread_started)

        else:
            self.tools.system_message(module = "framework", level = "debug", write = self.tools.values.NO_THREAD)
            self.handler = handler(self.__library)

        if not self.__booted_once:
            self.__booted_once = True

            for i in self.__library.modules.values():
                if hasattr(i, "start"): 
                    thread = self.__getThread()
                    thread.create_task(i.start)

        self.__loop.run_until_complete(self.__update_longpoll_server())                


    def start_polling(self) -> None:
        """
        Start polling VK longpoll server for any events
        """

        self.setup()
        self.__library.tools.system_message(module = "longpoll", level = "debug", write = self.tools.values.LONGPOLL_START)
        self.__loop.run_until_complete(self.__pollingCycle())


    def check(self, times: int = 1) -> None:
        """
        Check VK longpoll server for any events for number of times.

        times [int : 1] - how many times you need to check.
        """

        self.setup()

        self.tools.system_message(module = 'longpoll', level = "debug", write = self.tools.values.LONGPOLL_START)
        
        while times != 0:
            self.__loop.run_until_complete(self.__polling())
            times -= 1
        
        self.tools.system_message(module = 'longpoll', level = "debug", write = self.tools.values.LONGPOLL_CLOSE)


    async def __update_longpoll_server(self, update_ts: bool = True) -> None:
        response = await self.method('groups.getLongPollServer', {'group_id': self.__group_id})

        if update_ts: 
            self.__ts = response['ts']

        self.__longpoll_key = response['key']
        self.__longpoll_url = response['server']

        if self.tools.values.DEBUG_MESSAGES:
            self.tools.system_message( 
                module = "longpoll",
                level = "debug",
                write = self.tools.values.LONGPOLL_UPDATE)


    async def __check(self):
        values = {'act': 'a_check',
                'key': self.__longpoll_key,
                'ts': self.__longpoll_ts,
                'wait': 25,
                }
        
        response = await self.http.get(self.__longpoll_url, params = values)
        response = await response.json(content_type = None)

        if 'failed' not in response:
            self.__longpoll_ts = response['ts']

            return response['updates']

        elif response['failed'] == 1:
            self.__longpoll_ts = response['ts']

        elif response['failed'] == 2:
            await self.__update_longpoll_server(False)

        elif response['failed'] == 3:
            await self.__update_longpoll_server()

        return []


    async def __pollingCycle(self):
        while True: 
            await self.__polling()


    async def __polling(self):
        for event in await self.__check():
            if event['type'] == 'message_new':
                package = objects.package(event['object']['message'])

                package.params.client_info = objects.response(event['object']['client_info'])
                package.params.from_chat = package.peer_id > 2000000000

            else:
                package = objects.package(event['object'])

            package.type = getattr(events, event['type'])
            package.event_id = event['event_id']
            package.items = []

            self.__getThread().create_task(package)
        
    def __getThread(self):
        if len(self.__thread) > 0:
            self.__lastthread += 1
            
            if self.__lastthread == len(self.__thread):
                self.__lastthread = 0
            
            return self.__thread[self.__lastthread]

        else:
            return self.handler


    def test_parse(self, event: objects.package):
        """
        Init test parsing with received event 
        """
        self.setup()
        self.__getThread().create_task(event)




class tools:
    def __init__(self, group_id, api, http, assets, logger, level, print_log):
        self.__assets = _assets(assets)
        
        self.__logger = logger
        self.__log_level = level
        self.__print_log = print_log

        self.__http = http
        self.__api = api
        self.__group_id = group_id

        self.__waiting_replies = {}
        self.__group_address = asyncio.get_event_loop().run_until_complete(self.api.groups.getById(group_id=self.__group_id))[0].screen_name

        self.__group_mention = f'[club{self.__group_id}|@{self.__group_address}]'
        self.__mentions = [self.__group_mention]
        
        self.__values = global_expressions()


    class name_cases:
        nom = 'nom'
        gen = 'gen'
        dat = 'dat'
        acc = 'acc'
        ins = 'ins'
        abl = 'abl'


    @property
    def assets(self):
        return self.__assets


    @property
    def values(self):
        return self.__values


    @property
    def api(self):
        return self.__api


    @property
    def http(self):
        return self.__http


    def gen_random(self):
        return int(random.random() * 999999)


    def system_message(self, *args, write: typing.Optional[str] = None, module: str = "module", level:str = 'info', sep = " "):
        if not write:
            write = list(map(str, args))
            write = sep.join()

        write = "[" + level.upper() + "]\t" + "@" + self.__group_address + "." + module + ': ' + write
        if self.__print_log and logger_levels[level.upper()] >= self.__log_level:
            print(write)

        self.__logger.log(logger_levels[level.upper()], write)

            
    def getBotId(self):
        return -self.__group_id


    def getBotLink(self):
        return self.__group_address + ""


    def getBotDogMention(self):
        """
        Get Mention as testcanarybot.objects.mention
        To get mention at format [id|string] use repr(tools.getBotDogMention())
        """

        return objects.mention(self.__group_id, "@" + self.__group_address)


    def getBotMentions(self):
        """
        get all mentions that you set as bot mentions at commands
        """

        return self.__mentions[:]
    

    def wait_check(self, package):
        if package.type == events.message_new:
            return objects.task(package) in self.__waiting_replies.keys()

        else:
            raise TypeError("Only message_new")


    async def wait_reply(self, package):
        if package.type == events.message_new:
            wait = objects.task(package)
            self.__waiting_replies[wait] = False

            while not self.__waiting_replies[wait]:
                await asyncio.sleep(0)
                
            return self.__waiting_replies.pop(wait)

        else:
            raise TypeError("Only message_new")


    async def getMention(self, page_id: int, name_case: str = "nom", name: bool = True, last_name: bool = False):
        if name_case == 'link':
            name_case = 'nom'
            name = False
            last_name = False
            
        call = ""

        if page_id > 0:
            request = await self.__api.users.get(user_ids = page_id, name_case = name_case, fields = "screen_name")

            if name or last_name:

                if name:
                    call += request[0].first_name               # [id1|Павел]

                if name and last_name:                        # [id1|Павел Дуров]
                    call += " "

                if last_name:
                    call += request[0].last_name               # [id1|Дуров]

            else:
                if hasattr(request[0], 'screen_name'):
                    call = "@" + str(request[0].screen_name)    # [id1|@durov]

                else:
                    call = "@id" + str(page_id)                 # [id1|@id1]
            
            return f'[id{page_id}|{call}]'
        
        elif page_id == self.__group_id:
            return self.mentions_self[name_case]
        
        else:
            request = await self.__api.groups.getById(group_id = -page_id)

            if name:
                call += request[0].name

            else:
                call += request[0].screen_name
            
            return f'[club{-page_id}|{call}]' 


    async def getManagers(self, group_id = None):
        response = []

        if not group_id:
            group_id = self.__group_id

        else:
            group_id = int(group_id)

        resource = await self.__api.groups.getMembers(group_id = group_id, sort = 'id_asc', filter='managers')

        for item in resource.items:
            if item.role in ['administrator', 'creator', 'moderator']:
                response.append(item)

        return response


    async def isManager(self, from_id: int, group_id = None):
        if not group_id:
            group_id = self.__group_id
            
        else:
            group_id = int(group_id)

        response = await self.getManagers(group_id)
        response = [i.id for i in response]

        return from_id in response


    async def getChatManagers(self, peer_id: int):
        response = []
        resource = await self.__api.messages.getConversationMembers(peer_id = peer_id)

        for item in resource.items:
            if hasattr(item, 'is_admin'):
                if item.is_admin:
                    response.append(item.member_id)
            elif hasattr(item, 'is_owner'):
                if item.is_owner:
                    response.append(item.member_id)

        return response



    async def isChatManager(self, from_id, peer_id: int):
        return from_id in await self.getChatManagers(peer_id)


    async def getMembers(self, peer_id: int):
        response = []
        resource = await self.__api.messages.getConversationMembers(peer_id = peer_id)

        for item in resource.items:
            response.append(item.member_id)

        return response


    async def isMember(self, from_id: int, peer_id: int):
        return from_id in await self.getMembers(peer_id)


