from .framework._application import _app as app
from .framework._library import join
import threading
import string
import random
import platform
import os
import sys
import traceback
packaet_path_separator = "\\" if platform.system() == 'Windows' else "/"
packaet_manager_name = 'tppm'
packaet_manager_separator = "\t"

testcanarybot_name_data = {
    'keywords': {
    'name': 'TestCanarybot',
    'version': '1.3.1',
    'branch': 'dev'},
    'sep': ' '
}

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

access_token = '{token}'
group_id = {group}

service_token = '{service_token}'   # optional
api = '5.130'                       # optional
threads = 0                         # optional


MENTIONS = []
ADDITIONAL_MENTIONS = []
PRIVATE_LIST = []
ALL_MESSAGES = False
ADD_MENTIONS = False
LISTITEM = '*'

PRINT_LOG = False
LOGLEVEL = "INFO"       # CRITICAL/ERROR/WARNING/INFO/DEBUG/NOTSET

assets = 'assets'
library = 'library'


if testcanarybot.root_init(__name__, __file__): # False -> it was launched through tppm
    bot = testcanarybot.app(
        accessToken = access_token,
        groupId = group_id,
        serviceToken = service_token, apiVersion = api, countThread = threads, level = LOGLEVEL)

    bot.setMentions(MENTIONS)
    bot.setPrivateList(PRIVATE_LIST)

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
    
    
    @objects.ContextManager(commands = [\"test\"])
    async def ContextManagerHandler(self, tools: objects.tools, package: objects.package):
        await tools.send_reply(package, "Hello world!")
"""


def message(*args):
    write = " ".join([packaet_manager_name, *args])
    sys.stdout.write(write + "\n")

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

def getProjects(path: str):
    projects = []

    for directory in os.listdir(path):
        if os.path.isdir(packaet_path_separator.join([path,directory])) and directory not in ['testcanarybot', 'docs', 'tools', 'all', 'info', 'assets', 'library']:
            if 'root.py' in os.listdir(packaet_path_separator.join([path, directory])) and 'assets' in os.listdir(packaet_path_separator.join([path, directory])) and 'library' in os.listdir(packaet_path_separator.join([path, directory])):
                if not os.path.isdir(packaet_path_separator.join([path, directory, 'root.py'])) and os.path.isdir(packaet_path_separator.join([path, directory, 'assets'])) and os.path.isdir(packaet_path_separator.join([path, directory, 'library'])):
                    projects.append(directory)

    return projects

class threadBot(threading.Thread):
    def __init__(self, data, botname, assets, library, path = os.getcwd()):
        threading.Thread.__init__(self)
        self.path = path
        self.botname = botname
        self.accessToken = ""
        self.groupId = 0
        self.serviceToken = ""
        self.apiVersion = "5.126"
        self.countThread = 0
        
        for i in ["community_access", "community_token", "access", "access_token"]:
            if hasattr(data, i):
                self.accessToken = getattr(data, i)
                break

        for i in ["community_id", "group_id", "groupid"]:
            if hasattr(data, i):
                self.groupId = getattr(data, i)
                break
        
        for i in ["community_service", "service", "service_token"]:
            if hasattr(data, i):
                self.serviceToken = getattr(data, i)
                break
        
        for i in ["apiVersion", "api", "API"]:
            if hasattr(data, i):
                self.apiVersion = getattr(data, i)
                break

        for i in ["countThread", "countthread", "threads"]:
            if hasattr(data, i):
                self.countThread = getattr(data, i)
                break


        self.all_messages = data.ALL_MESSAGES if hasattr(data, 'ALL_MESSAGES') else None
        self.listitem = data.LISTITEM if hasattr(data, 'LISTITEM') else None
        self.mentions = []
        self.pl = []

        for i in ["mentions", "MENTIONS"]:
            if hasattr(data, i):
                self.mentions = getattr(data, i)
                break

        for i in ["privatelist", "private_list", "PRIVATELIST", "PRIVATE_LIST"]:
            if hasattr(data, i):
                self.pl = getattr(data, i)
                break

        self.print_log = data.PRINT_LOG if hasattr(data, 'PRINT_LOG') else False
        self.addt = data.ADDITIONAL_MENTIONS if hasattr(data, 'ADDITIONAL_MENTIONS') else []
        self.level = data.LOGLEVEL if hasattr(data, 'LOGLEVEL') else "info"
        self.assets = assets
        self.library = library
        
        for i in ["assets", "ASSETS"]:
            if hasattr(data, i):
                self.assets = getattr(data, i)
                break

        for i in ["library", "LIBRARY"]:
            if hasattr(data, i):
                self.library = getattr(data, i)
                break

        self.start()

    def exception_handler(self, loop, context):
        print(traceback.format_exc())
        quit()


    def run(self):
        self.bot = app(accessToken = self.accessToken, groupId = self.groupId, apiVersion = self.apiVersion, serviceToken = self.serviceToken, level = self.level, print_log = self.print_log, path = self.path, countThread = self.countThread, assets = self.botname + packaet_path_separator + self.assets, library = self.botname + packaet_path_separator + self.library)
        
        if len(self.mentions) != 0: self.bot.setMentions(self.mentions)
        if len(self.pl) != 0: self.bot.setPrivateList(self.pl)
        if len(self.addt) != 0: self.bot.tools.values.set('ADDITIONAL_MENTIONS', self.addt)
        if self.all_messages: self.bot.tools.values.set("ALL_MESSAGES", self.all_messages)
        if self.listitem: self.bot.tools.values.set("LISTITEM", self.listitem)
        message("@" + self.bot.tools.getBotLink(), "initialised, started")
        self.bot.start_polling()