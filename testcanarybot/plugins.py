from .tools import *
import os
import importlib

class plugins():
    def __init__(self, v, group_id, api, library):
        self.v = v
        self.api = api
        self.library = library

        self.assets = assets()
        self.tools = tools(group_id, api)

        self.all = [i for i in self.getPlugins()]
        self.plugins = self.upload(self.all)


    def getPlugins(self):
        try:
            lib = os.listdir(self.library)

            lib.append('canarycore')

            if 'sampleplugin' in lib:
                lib.remove('sampleplugin')
            return lib

        except Exception as e:
            print(e)
            return ['canarycore']
        

    def upload(self, all):
        pl = {}

        for plugin in all:
            if plugin != 'canarycore':
                print(f"Loading: {plugin}", end="... ")
                try:
                    pluginObj = getattr(importlib.import_module("library." + plugin + ".main"), 'lib_plugin')()
                except Exception as e:
                    print(f"Broken ({e})")
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
            else:
                from .core import lib_plugin
                pl[plugin] = lib_plugin()
                
        return pl

    def error_handler(self, peer_id, response):
        if len(response) == 0:
            self.api.messages.send(random_id = random.randint(0,999999), peer_id = peer_id, message = 'Можешь повторить?', attachment='photo-195675828_457241495')
        else:
            for i in response:
                if type(i) is str:
                    if i.startswith('console: '):
                        code = i[9:]
                        try:
                            exec(code)
                        except Exception as e:
                            self.api.messages.send(random_id = random.randint(0,999999), peer_id = peer_id, message = f'{e} ({i})')
                    elif i.startswith('plugins: '):
                        code = i[9:]
                        if code in self.all:
                            descr = self.plugins[code].descr if self.plugins[code].descr else 'Модуль без описания.'
                            self.api.messages.send(random_id = random.randint(0,999999), peer_id = peer_id, message = f"Описание {code}: {descr}")
                        else:
                            if len(self.all) > 1:
                                response = 'Библиотека, с которой работает Canarybot:\n'
                                for plugin in self.all:
                                    response += '\n\u2022 ' + plugin if plugin != 'canarycore' else ''
                                response += '\n\nЧтобы получить описание модуля, отправьте @canarybot ассеты описание {название модуля}'
                            else:
                                response = 'В данный момент в библиотеке ничего нет :/'
                            
                            self.api.messages.send(random_id = random.randint(0,999999), peer_id = peer_id, message = response, attachment='photo-195675828_457241499')

    def parse_command(self, messagetoreact):
        for i in ['chat_invite_user', 'chat_kick_user', self.tools.endline]:
            messagetoreact = messagetoreact.replace(i, 'system_message')
        
        response = []
        message = messagetoreact.split()


        if len(message) > 1:
            if message[0] in [*self.tools.mentions, 'console']:
                if message[0] in self.tools.mentions: message.pop(0)

                for i in message:
                    response.append(self.tools.parse_mention(i[1:-1]) if i[0] == '[' and i[-1] == ']' and i.count('|') == 1 else i)

            elif self.tools.group_mention in message:
                response.append(self.tools.mention)
                
        elif message[0] == self.tools.group_mention:
            response.append(self.tools.mention)
        response.append(self.tools.endline)

        return response

    def parse(self, message):
        response = []
        
        for plugin in self.plugins.values():
            result = plugin.update(self.api, self.tools, message)
            if result: response.append(result)

        self.error_handler(message.peer_id, response)

