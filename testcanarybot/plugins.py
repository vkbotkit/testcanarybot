from .tools import *
import os
import traceback
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
        
        for name in ['sampleplugin', '__pycache__']:
            if name in response: response.remove(name)

        self.tools.system_message(self.tools.getObject("PLUGIN_LOAD"))

        return response
        

    def upload(self, all):
        pl = {}

        for plugin in all:
            if plugin != 'canarycore':
                self.tools.plugin = plugin
                self.tools.system_message(self.tools.getObject("PLUGIN_INIT"))

                try:
                    if plugin.endswith('.py'):
                        pluginObj = importlib.import_module("library." + plugin[:-3])
                        pluginObj.init(self.tools)
                    
                    else:
                        pluginObj = importlib.import_module("library." + plugin + ".main")
                        pluginObj.init(self.tools)
                    
                except Exception as e:
                    self.tools.system_message(self.tools.getObject("PLUGIN_FAILED_BROKEN").format(e))
                    self.all = [i for i in self.all if i != plugin]

                    continue

                if pluginObj.v not in self.supp_v:
                    self.tools.system_message(self.tools.getObject("PLUGIN_FAILED_NOSUPP"))
                    self.all = [i for i in self.all if i != plugin]

                elif not hasattr(pluginObj, 'name'):
                    tools.system_message(self.tools.getObject("PLUGIN_FAILED_NONAME"))
                    self.all = [i for i in self.all if i != plugin]

                elif not hasattr(pluginObj, 'descr'):
                    tools.system_message(self.tools.getObject("PLUGIN_FAILED_NODESCR"))
                    self.all = [i for i in self.all if i != plugin]

                elif not hasattr(pluginObj, 'update'):
                    tools.system_message(self.tools.getObject("PLUGIN_FAILED_NOUPD"))
                    self.all = [i for i in self.all if i != plugin]
                
                else:
                    pl[plugin] = pluginObj

            else:
                from . import core as lib_plugin

                self.tools.plugin = 'canarycore'
                self.tools.system_message(self.tools.getObject("PLUGIN_INIT"))
                
                lib_plugin.init(self.tools)
                pl[plugin] = lib_plugin
                
        return pl


    def error_handler(self, package, reaction):
        package['plugintype'] = self.tools.objects.events.ERROR_HANDLER

        if len(reaction) == 0:
            reaction.append([self.tools.getObject("NOREACT")])

        for i in reaction:
            if isinstance(i, list):
                package['text'] = i

                try:
                    if package['text'][0] == self.tools.getObject("LIBRARY_SYNTAX"):
                        if package['text'][1] == self.tools.getObject("LIBRARY_NOSELECT"):
                            package['text'][1] = self.all

                        elif package['text'][1] in self.all:
                            package['text'].append(self.plugins[package['text'][1]].v)
                            package['text'].append(self.plugins[package['text'][1]].descr)

                            if hasattr(self.plugins[package['text'][1]], "name"):
                                package['text'][1] = self.plugins[package['text'][1]].name

                        else:
                            package['text'][1] = self.tools.getObject("LIBRARY_ERROR")

                    elif package['text'][0] == self.tools.getObject("PARSER_SYNTAX"):
                        for message in package['text'][1:-1]:
                            message['from_id'] = package['from_id']
                            message['peer_id'] = package['peer_id']

                            if 'fwd_messages' in message: message['fwd_messages'] = None
                            if 'reply_message' in message: message['reply_message'] = None

                            self.parse(message)

                        del package['text'][1:]

                        package['text'].append(self.tools.getObject("FWD_MES"))
                        package['text'].append(self.tools.getObject("ENDLINE"))

                    for key, plugin in self.plugins.items():
                        self.tools.plugin = key
                        
                        if plugin.plugintype == package['plugintype'] or package['plugintype'] in plugin.plugintype:
                            plugin.update(self.tools, package)

                except Exception as e:
                    self.tools.system_message(traceback.format_exc())

        self.tools.plugin = "message_handler"
        self.tools.system_message(f"chat{package['peer_id']}-{package['from_id']}: {package['text'][:-1]}")


    def reload(self):
        self.all = [i for i in self.getPlugins()]
        self.plugins = self.upload(self.all)
        

    def send(self, event):
        if str(event.type) == self.tools.events.MESSAGE_NEW:
            self.parse(event.object['message'])

        else:
            event.type = str(event.type).upper()

            if event.type in self.tools.objects.events.list_of_types:
                package = self.tools.objects.object_handler(self.tools, event.type, event.object)
                self.parse_package(package)
        

    def parse(self, message):
        message['plugintype'] = self.tools.objects.events.MESSAGE_NEW

        if 'action' in message:
            message['text'] = self.parse_action(message['action'])
            self.parse_package(message)

        elif 'payload' in message:
            message['text'] = self.parse_payload(message['payload'])
            self.parse_package(message)

        elif 'text' in message:
            if message['text'] != '':
                message['text'] = self.parse_command(message['text'])
                
                if message['text'][0] != self.tools.getObject("ENDLINE"):
                    self.parse_package(message)


    def parse_mention(self, mention):
        response = mention.replace(mention[mention.find('|'):], '')

        response = response.replace('id', '')
        response = response.replace('club', '-')
        response = response.replace('public', '-')
            
        return int(response)


    def parse_link(self, link):
        response = link

        for i in ['https://', 'http://']:
            if i in response: response.replace(i, '')
        
        if response.startswith('vk.com/'):
            response = response.replace('vk.com/', '')
            
            try:
                response_util = self.api.utils.resolveScreenName(screen_name = response)

                if response_util['type'] == 'user':
                    response = response_util['object_id']

                elif response['type'] == 'group':
                    response = -response_util['object_id']

                elif response['type'] == 'vk_app':
                    response = f"vk_app-{response_util['object_id']}"

                else:
                    response = 'vk.com/' + response_util

            except Exception as e:
                pass
        
        return response


    def parse_payload(self, messagepayload):
        response = [self.tools.getObject("PAYLOAD")]

        response.append(json.loads(messagepayload))
        response.append(selftools.getObject("ENDLINE"))
        
        return response


    def parse_action(self, messageaction):
        response = [self.tools.getObject("ACTION")]

        response.extend(messageaction.values())
        response.append(self.tools.getObject("ENDLINE"))

        return response


    def parse_command(self, messagetoreact):
        for i in self.tools.objects.exp.list_of_exp:
            value = getattr(self.tools.objects.exp, i)

            if type(value) is str and value in messagetoreact:
                messagetoreact = messagetoreact.replace(i, 'system_message')

        response = []
        message = messagetoreact.split()

        if len(message) > 1:
            if message[0] in [*self.tools.getObject("MENTIONS")]:
                message.pop(0)

                for i in message:
                    if i[0] == '[' and i[-1] == ']' and i.count('|') == 1:
                        response.append(self.parse_mention(i[1:-1]))

                    else:
                        response.append(self.parse_link(i))

        elif response == []:
            for word in message:
                if word.lower() in [*self.tools.getObject("MENTIONS"), 
                                    *self.tools.getObject("MENTION_NAME_CASES")]: 
                    response.append(self.tools.getObject("MENTION"))

        response.append(self.tools.getObject("ENDLINE"))

        return response


    def parse_package(self, package):
        response = []

        for key, plugin in self.plugins.items():
            self.tools.plugin = key

            if plugin.plugintype == package['plugintype'] or package['plugintype'] in plugin.plugintype:
                result = plugin.update(self.tools, package)

                if result: 
                    response.append(result)
                    
        self.error_handler(package, response)