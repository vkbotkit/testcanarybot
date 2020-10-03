import six
import os
import importlib
import random

group_id = 0
group_mention = ''
shortname = ''


class plugins_autoimport():
    __slots__ = ('name', 'method', 'all')
    def __init__(self, method = None):
        self.method = method
        self.name = method


    def __getattr__(self, method):
        self.name = (self.method + '.' if self.method else '') + method
        return lib_plugins(self.name)


    def __call__(self, **kwargs):
        for k, v in six.iteritems(kwargs):
            if isinstance(v, (list, tuple)):
                kwargs[k] = ','.join(str(x) for x in v)
        try:
            test = getattr(
                importlib.import_module(
                        "library."+ (self.name[0:self.name.rfind('.')]) + ".main"
                    ), 
                self.name[self.name.rfind('.')+1:]
            )(kwargs)

        except Exception as e:
            print(e)

class plugins():
    def __init__(self, v, assets, tools, api):
        self.v = v
        self.all = [i for i in self.getPlugins() if i != 'tools']
        self.plugins = self.upload(self.all)
        self.assets = assets
        self.api = api
        self.tools = tools


    def getPlugins(self):
        try:
            return os.listdir(os.path.abspath(os.path.dirname(__file__)) + '\\library\\')
        except Exception as e:
            print(e)
            return []
        

    def upload(self, all):
        pl = {}

        for plugin in all:
            if plugin != 'tools':
                print(f"Loading: {plugin}", end="... ")
                try:
                    pluginObj = getattr(importlib.import_module("library." + plugin + ".main"), 'lib_plugin')()
                except Exception as e:
                    print(f"Broken")

                    self.all = [i for i in self.all if i != plugin]
                    continue

                if pluginObj.v != self.v:
                    print(f"Did not match versions")
                    self.all = [i for i in self.all if i != plugin]

                elif not hasattr(pluginObj, 'update'):
                    print(f"No 'update' function")
                    self.all = [i for i in self.all if i != plugin]
                
                else:
                    pl[plugin] = pluginObj
                    print(f"Loaded")
        return pl

    def error_handler(self, peer_id, response):
        if len(response) == 0:
            self.api.messages.send(random_id = random.randint(0,999999), peer_id = peer_id, message = 'Можешь повторить?', attachment='photo-195675828_457241495')
        else:
            for i in response:
                if type(i) is not int:
                    print(i)


    def parse(self, message):
        response = []
        for plugin in self.plugins.values():
            result = plugin.update(self.api, self.tools, message)
            if result: response.append(result)

        self.error_handler(message.peer_id, response)


class tools:
    def __init__(self, api):
        self.api = api
        
    def getMention(self, page:int, nc = None):
        if nc == 'link':
            if page > 0:
                return f'[id{page}|@id{page}]'
            else:
                return f'[club{-page}|@{self.api.groups.getById(group_id = -page)[0]["screen_name"]}]'
        else:
            if page > 0:
                return f'[id{page}|{self.api.users.get(user_ids = page, name_case=nc)[0]["first_name"]}]'
            else:
                return f'[club{-page}|{self.api.groups.getById(group_id = -page)[0]["name"]}]' 


def upd_id(number, api):
    global group_id
    global group_mention
    global shortname
    group_id = number
    group_mention = f'[club{group_id}|@canarybot]'
    shortname = api.groups.getById(group_id=group_id)[0]['screen_name']


def parse_mention(mentiontoparse):
    mention = mentiontoparse.replace(mentiontoparse[mentiontoparse.find('|'):], '')

    mention = mention.replace('id', '')
    mention = mention.replace('club', '-')
    mention = mention.replace('public', '-')
        
    return int(mention)


def parse_action(messageaction):
    response = []
    response.extend(messageaction.values())
    response.append(':::CANARYBOT:endmessage:::')
    return response

def parse_command(messagetoreact):

    message = messagetoreact
    response = []
    for i in ['chat_invite_user', 'chat_kick_user', ':::CANARYBOT:mention:::']:
        message = message.replace(i, 'system_message')
    
    message = message.split()

    if group_mention in message:
        if message[0] == group_mention and len(message) > 1:
            message.pop(0)
            for i in message:
                if i[0] == '[' and i[-1] == ']' and i.count('|') == 1:
                    response.append(parse_mention(i[1:-1]))
                else:
                    response.append(i)
        else:
            response.append(':::CANARYBOT:mention:::')
    response.append(':::CANARYBOT:endmessage:::')
    return response

class assets():
    """
    lib_assets(filename, mode): open path.
    """


    def __call__(self, filename, mode):
        return open(os.path.abspath(os.path.dirname(__file__)) + '\\assets\\' + filename, mode)


if __name__ == "__main__":
    # Подключение файла из папки library 
    # testlib = plugins_autoimport()
    # testlib.package.update() #library/package/main.py update()

    # Подключение медиафайла из папки assets
    # testassets = assets()

    # test2 = open('test.jpg', "wb")
    # with testassets('test.jpg', "rb") as origin:
    #     test2.write(origin.read())

    # v = '002'
    # token = ""


    # Список плагинов
    # testplugins = plugins(v, testassets, api)
    
    # print(testplugins.plugins)
    # print(testplugins.all)
    # print(testplugins.getPlugins())

    # print(testplugins.getMention(517114114, 'nom'))
    pass