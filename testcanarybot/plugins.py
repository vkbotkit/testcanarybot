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

        self.tools.system_message(self.tools.objects.PLUGIN_LOAD)
        return response
        

    def upload(self, all):
        pl = {}

        for plugin in all:
            if plugin != 'canarycore':
                self.tools.plugin = plugin
                self.tools.system_message(self.tools.objects.PLUGIN_INIT)
                try:
                    if plugin.endswith('.py'):
                        pluginObj = getattr(importlib.import_module("library." + plugin[:-3]), 'lib_plugin')(self.api, self.tools)
                    
                    else:
                        pluginObj = getattr(importlib.import_module("library." + plugin + ".main"), 'lib_plugin')(self.api, self.tools)
                    
                except Exception as e:
                    self.tools.system_message(self.tools.objects.PLUGIN_FAILED_BROKEN.format(e))
                    self.all = [i for i in self.all if i != plugin]
                    continue

                if pluginObj.v not in self.supp_v:
                    self.tools.system_message(self.tools.objects.PLUGIN_FAILED_NOSUPP)
                    self.all = [i for i in self.all if i != plugin]

                elif not hasattr(pluginObj, 'update'):
                    tools.system_message(self.tools.objects.PLUGIN_FAILED_NOUPD)
                    self.all = [i for i in self.all if i != plugin]
                
                else:
                    pl[plugin] = pluginObj

            else:
                from .core import lib_plugin
                self.tools.plugin = 'system'
                self.tools.system_message(self.tools.objects.PLUGIN_INIT)
                pl[plugin] = lib_plugin(self.api, self.tools)
                
        return pl


    def error_handler(self, package, reaction):
        package['plugintype'] = self.tools.objects.ERROR_HANDLER

        if len(reaction) == 0:
            reaction.append([self.tools.objects.NOREACT])

        for i in reaction:
            if type(i) is list:
                package['text'] = i

                try:
                    if package['text'][0] == self.tools.objects.LIBRARY_SYNTAX:
                        if package['text'][1] == self.tools.objects.LIBRARY_NOSELECT:
                            package['text'][1] = self.all

                        elif package['text'][1] in self.all:
                            package['text'].append(self.plugins[package['text'][1]].descr)

                        else:
                            package['text'][1] = self.tools.objects.LIBRARY_ERROR

                    self.plugins['canarycore'].update(self.api, self.tools, package)

                except Exception as e:
                    print(traceback.format_exc())


    def reload(self):
        self.all = [i for i in self.getPlugins()]
        self.plugins = self.upload(self.all)
        

    def send(self, event):
        if event.type == self.tools.objects.MESSAGE_NEW:
            self.parse(event.object['message'])

        elif event.type == 'like_add':
            package = {}
            package['text'] = []
            package['plugintype'] = self.tools.objects.LIKE_ADD
            package['text'].append(event.object)

            self.parse_package(package)

        elif event.type == 'like_remove':
            package = {}
            package['text'] = []
            package['plugintype'] = self.tools.objects.LIKE_REMOVE
            package['text'].append(event.object)

            self.parse_package(package)
            
        else:
            return None
        

    def parse(self, message):
        message['plugintype'] = self.tools.objects.MESSAGE_NEW
        if 'action' in message:
            message['text'] = self.parse_action(message['action'])
            self.parse_package(message)

        elif 'payload' in message:
            message['text'] = self.parse_payload(message['payload'])
            self.parse_package(message)

        elif 'text' in message:
            if message['text'] != '':
                message['text'] = self.parse_command(message['text'])

                if message['text'][0] != self.tools.objects.ENDLINE:
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
        response = [self.tools.objects.PAYLOAD]
        response.append(json.loads(messagepayload))
        response.append(self.tools.objects.ENDLINE)
        
        return response


    def parse_action(self, messageaction):
        response = [self.tools.objects.ACTION]

        response.extend(messageaction.values())
        response.append(self.tools.objects.ENDLINE)

        return response


    def parse_command(self, messagetoreact):
        for i in self.tools.objectslist:
            value = getattr(self.tools.objects, i)

            if type(value) is str and value in messagetoreact:
                messagetoreact = messagetoreact.replace(i, 'system_message')

        response = []
        message = messagetoreact.split()

        if len(message) > 1:
            if message[0] in [
                *self.tools.objects.MENTION, 
                *self.tools.objects.CONSOLE_COMMANDS
                ]:
                if message[0].lower() in self.tools.objects.MENTION: 
                    message.pop(0)

                for i in message:
                    if i[0] == '[' and i[-1] == ']' and i.count('|') == 1:
                        response.append(self.parse_mention(i[1:-1]))

                    else:
                        response.append(self.parse_link(i))

            else:
                for word in message:
                    if word.lower() in [
                        *self.tools.objects.MENTION, 
                        *self.tools.objects.MENTION_NAME_CASES
                        ]: 
                        response.append(self.tools.objects.MENTION)
                
        elif message[0] == self.tools.group_mention:
            response.append(self.tools.objects.MENTION)

        response.append(self.tools.objects.ENDLINE)

        return response


    def parse_package(self, package):
        response = []
        for key, plugin in self.plugins.items():
            self.tools.plugin = key

            if hasattr(plugin, 'plugintype'):
                if plugin.plugintype == package['plugintype'] or package['plugintype'] in plugin.plugintype:
                    result = plugin.update(self.api, self.tools, package)

                    if result: 
                        response.append(result)
            
            elif package['plugintype'] == self.tools.objects.MESSAGE_NEW:
                result = plugin.update(self.api, self.tools, package)

                if result: 
                    response.append(result)

        self.error_handler(package, response)