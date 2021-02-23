from .. import exceptions
from .. import objects


import asyncio
import importlib
import os


class library:
    modules = {}
    handlers = {
        'void': [], # [handler1, handler2]
        'priority': {}, # {'test', 'hello', 'world'}: [handler1, handler2, ...]
        'events': {}, # event.abstract_event: [handler1, handler2]
        'action': {}
    }

    def __init__(self, tools):
        self.tools = tools
        self.list = []
        self.void_react = False
        self.commands = []
            

    def upload(self, isReload = False, loop = asyncio.get_event_loop()):
        self.modules = {}

        if 'library' in os.listdir(os.getcwd()):
            self.tools.system_message(str(self.tools.values.LIBRARY_GET), module = "library.uploader")
            
            listdir = [i for i in os.listdir(os.getcwd() + '\\library\\') if i != "__pycache__" and (i.endswith('.py') or i.count(".") == 0)]

            if len(listdir) == 0:
                raise exceptions.LibraryError(
                    self.tools.values.LIBRARY_ERROR)

            loop.run_until_complete(asyncio.wait([loop.create_task(self.upload_handler(module)) for module in listdir]))
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
                    await coro()

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
        
        if len(moduleObj.action_handlers.keys()) > 0:
            for action in moduleObj.action_handlers.keys():
                message += self.tools.values.MODULE_INIT_ACTION.value.format(event = str(action))

                if not action in self.handlers['action']:
                    self.handlers['action'][action] = []
                self.handlers['action'][action].extend(moduleObj.action_handlers[action])

        if moduleObj.void_react:
            self.handlers['void'].append(moduleObj.void_react)
            self.void_react = True
            message += self.tools.values.MODULE_INIT_VOID.value

        self.modules[module_name] = moduleObj
        self.list = module_name
        return self.tools.system_message(write = message, module = "library.uploader")
