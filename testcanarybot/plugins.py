from .tools import *
import os
import importlib
import json

class plugins():
    def __init__(self, v, group_id, api, getPath):
        self.supp_v = v
        self.api = api
        self.library = getPath + '\\library\\'

        self.tools = tools(getPath + '\\assets\\', group_id, api)

        self.all = self.getPlugins()
        self.plugins = self.upload(self.all)


    def getPlugins(self):
        self.tools.plugin = 'getPlugins'
        response = ['canarycore']

        try:
            response.extend(os.listdir(self.library))
        except Exception as e:
            self.tools.system_message(e)
            
        if 'sampleplugin' in response: response.remove('sampleplugin')

        self.tools.system_message('plugin list is loaded, to update use "self.all = self.getPlugins()"')
        return response
        

    def upload(self, all):
        pl = {}

        for plugin in all:
            if plugin != 'canarycore':
                self.tools.plugin = plugin
                self.tools.system_message('initialization... ')
                try:
                    pluginObj = getattr(importlib.import_module("library." + plugin + ".main"), 'lib_plugin')(self.api, self.tools)
                except Exception as e:
                    self.tools.system_message(f"Broken ({e})")
                    self.all = [i for i in self.all if i != plugin]
                    continue

                if pluginObj.v not in self.supp_v:
                    tools.system_message("Plugin version isn't supported")
                    self.all = [i for i in self.all if i != plugin]

                elif not hasattr(pluginObj, 'update'):
                    tools.system_message("No 'update' function")
                    self.all = [i for i in self.all if i != plugin]
                
                else:
                    pl[plugin] = pluginObj
            else:
                from .core import lib_plugin
                self.tools.plugin = 'system'
                self.tools.system_message('Loading... ')
                pl[plugin] = lib_plugin(self.api, self.tools)
                
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
                                response = f'Библиотека, с которой работает {self.tools.group_mention}:\n'
                                for plugin in self.all:
                                    response += '\n\u2022 ' + plugin if plugin != 'canarycore' else ''
                                response += '\n\nЧтобы получить описание модуля, отправьте @canarybot ассеты описание {название модуля}'
                            else:
                                response = 'В данный момент в библиотеке ничего нет :/'
                            
                            self.api.messages.send(random_id = random.randint(0,999999), peer_id = peer_id, message = response, attachment='photo-195675828_457241499')

    def reload(self):
        self.all = [i for i in self.getPlugins()]
        self.plugins = self.upload(self.all)
        
        
    def parse_mention(self, mentiontoparse):
        mention = mentiontoparse.replace(mentiontoparse[mentiontoparse.find('|'):], '')

        mention = mention.replace('id', '')
        mention = mention.replace('club', '-')
        mention = mention.replace('public', '-')
            
        return int(mention)

    def parse_payload(self, messagepayload):
        response = [self.tools.payload]
        response.append(json.loads(messagepayload))
        return response

    def parse_action(self, messageaction):
        response = []

        response.append(self.tools.action)
        response.extend(messageaction.values())
        response.append(self.tools.endline)

        return response

    def parse_command(self, messagetoreact):
        for i in [self.tools.action, self.tools.mention, self.tools.endline]:
            messagetoreact = messagetoreact.replace(i, 'system_message')
        
        response = []
        message = messagetoreact.split()


        if len(message) > 1:
            if message[0] in [*self.tools.mentions, 'console']:
                if message[0] in self.tools.mentions: message.pop(0)

                for i in message:
                    response.append(self.parse_mention(i[1:-1]) if i[0] == '[' and i[-1] == ']' and i.count('|') == 1 else i)

            elif self.tools.group_mention in message:
                response.append(self.tools.mention)
                
        elif message[0] == self.tools.group_mention:
            response.append(self.tools.mention)
        response.append(self.tools.endline)

        return response

    def parse(self, message):
        response = []

        for key, plugin in self.plugins.items():
            self.tools.plugin = key
            result = plugin.update(self.api, self.tools, message)
            if result: response.append(result)

        self.error_handler(message['peer_id'], response)