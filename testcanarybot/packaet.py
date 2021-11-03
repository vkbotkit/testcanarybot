from .framework._application import _app as app
import threading
import traceback
import string
import random
import os


# Copyright 2021 kensoi


packaet_manager_name = '[tppm]'
packaet_manager_separator = '\t'

packaet_readme_assets = """testcanarybot assets
Copyright 2021 kensoi

Usage: with tools.assets(*args) as file: #like open(*args, **kwargs)
    #file usage"""
packaet_readme_library = """testcanarybot library
Copyright 2021 kensoi

Create module: python testcanarybot --project {packaet_project_directory} --cm HandlerName"""

packaet_root_raw = """'''
testcanarybot project root
Copyright 2021 kensoi

This is raw created root file for testcanarybot project.
fill all important info and try to run with "$ python testcanarybot --run [LIST OF PROJECT DIRECTORIES]"

'''

import testcanarybot

community_token = '{token}'
community_id = {group}

community_service = '{service_token}' # optional
apiVersion = '5.131'    # optional
countThread = 0         # optional


MENTIONS = []
ADDITIONAL_MENTIONS = []
ALL_MESSAGES = False
ADD_MENTIONS = False
LISTITEM = '*'

PRINT_LOG = False
LOGLEVEL = "INFO"       # CRITICAL/ERROR/WARNING/INFO/DEBUG/NOTSET

assets = 'assets'
library = 'library'


if testcanarybot.root_init(__name__, __file__): # False -> it was launched through tppm
    bot = testcanarybot.app(
        accessToken = community_token,
        groupId = community_id,
        serviceToken = community_service, apiVersion = apiVersion, countThread = countThread, level = LOGLEVEL)

    bot.setMentions(MENTIONS)

    bot.tools.values.set("ALL_MESSAGES", ALL_MESSAGES)
    bot.tools.values.set("ADD_MENTIONS", ADD_MENTIONS)
    bot.tools.values.set("LISTITEM", LISTITEM)
    bot.tools.values.set('ADDITIONAL_MENTIONS', ADDITIONAL_MENTIONS)

    bot.start_polling()
"""

libraryModuleRaw = """'''
library module raw script
Copyright 2021 kensoi
'''
from testcanarybot import objects


class Main(objects.libraryModule):
    async def start(self, tools: objects.tools):
        pass # create task at start
    
    
    
    @objects.ContextManager(commands = [\"check\"])
    async def ContextManagerHandler(self, tools: objects.tools, package: objects.package):
        await tools.api.message.send(
            random_id = tools.gen_random(), 
            peer_id = package.peer_id, 
            message = "Hello world!"
            )
"""


def system_message(*args):
    print(packaet_manager_name, packaet_manager_separator, *args)

def gen_str(test = None):
    result, num = "", random.randint(5, 25)

    if isinstance(test, int):
        num = test

    while num != 0:
        result += random.choice([*string.ascii_lowercase, *string.digits])
        num -= 1

    return result

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

def getProjects(path: str):
    projects = []

    for directory in os.listdir(path):
        if os.path.isdir('\\'.join([path,directory])) and directory not in ['testcanarybot', 'docs', 'tools', 'all', 'info', 'assets', 'library']:
            if 'root.py' in os.listdir('\\'.join([path, directory])) and 'assets' in os.listdir('\\'.join([path, directory])) and 'library' in os.listdir('\\'.join([path, directory])):
                if not os.path.isdir('\\'.join([path, directory, 'root.py'])) and os.path.isdir('\\'.join([path, directory, 'assets'])) and os.path.isdir('\\'.join([path, directory, 'library'])):
                    projects.append(directory)

    return projects

class threadBot(threading.Thread):
    def __init__(self, data, botname, assets, library, path = os.getcwd()):
        threading.Thread.__init__(self)
        self.path = path
        self.botname = botname
        self.accessToken = data.community_token + ""
        self.groupId = data.community_id + 0
        self.serviceToken = "" if not hasattr(data, 'community_service') else data.community_service + ""
        self.apiVersion = "5.126" if not hasattr(data, 'apiVersion') else data.apiVersion + ""
        self.countThread = 5 if not hasattr(data, 'countThread') else data.countThread + 0

        self.all_messages = data.ALL_MESSAGES if hasattr(data, 'ALL_MESSAGES') else None
        self.listitem = data.LISTITEM if hasattr(data, 'LISTITEM') else None

        self.mentions = data.MENTIONS[:] if hasattr(data, 'MENTIONS') else []
        self.mentions = data.mentions[:] if hasattr(data, 'mentions') else []
        self.print_log = data.PRINT_LOG if hasattr(data, 'PRINT_LOG') else False
        self.addt = data.ADDITIONAL_MENTIONS if hasattr(data, 'ADDITIONAL_MENTIONS') else []
        self.level = data.LOGLEVEL if hasattr(data, 'LOGLEVEL') else "info"
        self.assets = data.assets if hasattr(data, 'assets') else assets
        self.library = data.library if hasattr(data, 'library') else library
        self.assets = data.ASSETS if hasattr(data, 'ASSETS') else assets
        self.library = data.LIBRARY if hasattr(data, 'LIBRARY') else library

        self.start()

    def exception_handler(self, loop, context):
        print(traceback.format_exc())
        quit()


    def run(self):
        self.bot = app(accessToken = self.accessToken, groupId = self.groupId, apiVersion = self.apiVersion, serviceToken = self.serviceToken, level = self.level, print_log = self.print_log, path = self.path, countThread = self.countThread, assets = self.botname + '\\' + self.assets, library = self.botname + '\\' + self.library)
        
        if len(self.mentions) != 0: 
            self.bot.setMentions(self.mentions)

        if len(self.addt) != 0: 
            self.bot.tools.values.set('ADDITIONAL_MENTIONS', self.addt)

        if self.all_messages: 
            self.bot.tools.values.set("ALL_MESSAGES", self.all_messages)

        if self.listitem: 
            self.bot.tools.values.set("LISTITEM", self.listitem)
        
        system_message("@" + self.bot.tools.getBotLink(), "initialised, started")
        self.bot.start_polling()