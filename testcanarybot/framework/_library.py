from .. import exceptions
from .. import objects


import asyncio
import importlib
import os
import sys

class library:
    def __init__(self, tools, library):
        self.botname = library
        self.tools = tools
        self.list = []
        self.void_react = False
        self.commands = []
        self.raw_modules = []
        
        self.modules = {}
        self.handlers = {
            'void': [], # [handler1, handler2]
            'priority': {}, # {'test', 'hello', 'world'}: [handler1, handler2, ...]
            'events': {}, # event.abstract_event: [handler1, handler2]
            'action': {}
        }
            

    def upload(self, isReload = False, loop = asyncio.get_event_loop()):

        if len(self.raw_modules) > 0:
            for i in self.raw_modules:
                importlib.reload(i)
        else:
            self.modules = {}
            if os.path.isdir(self.botname + 'library\\'):
                self.tools.system_message(str(self.tools.values.LIBRARY_GET), module = "library.uploader")
            
                listdir = [i for i in os.listdir(self.botname + 'library\\' + '\\') if i != "__pycache__" and (i.endswith('.py') or i.count(".") == 0)]

                if len(listdir) == 0:
                    raise exceptions.LibraryError(
                        self.tools.values.LIBRARY_ERROR)
                loop.run_until_complete(asyncio.wait([loop.create_task(self.upload_handler(module)) for module in listdir]))
                self.tools.system_message(
                    "Supporting event types: {event_types}".format(
                        event_types = "\n".join(["", "\t\tevents.message_new", *["\t\t" + str(i) for i in self.handlers['events'].keys()], ""])
                    ), module = "library.uploader", level = "info")

            else:
                raise RuntimeError("broken project.")
        

    async def upload_handler(self, module_name):
        module_direct = self.botname + 'library\\' + module_name
        if module_direct.endswith('.py'):
            pass
        else:
            module_direct += '\\main.py'
        module_name = module_direct[:-3].replace('\\', '.')
        module = importlib.import_module(module_name)
        self.raw_modules.append(module)

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
                    if j in self.handlers['priority']:
                        raise exceptions.LibraryRewriteError(f"[{module_name}] `{str(j)}` is already registered command")
                    else:
                        self.handlers['priority'][j] = i['handler']

        if len(moduleObj.event_handlers.keys()) > 0:
            for event in moduleObj.event_handlers.keys():
                message += self.tools.values.MODULE_INIT_EVENTS.value.format(event = str(event))
                if event in self.handlers['events']:
                    raise exceptions.LibraryRewriteError(f"[{module_name}] `{str(action)}`is already registered void")
                else:
                    self.handlers['events'][event] = moduleObj.event_handlers[event]
        
        if len(moduleObj.action_handlers.keys()) > 0:
            for action in moduleObj.action_handlers.keys():
                message += self.tools.values.MODULE_INIT_ACTION.value.format(event = str(action))

                if action in self.handlers['action']:
                    raise exceptions.LibraryRewriteError(f"[{module_name}] `{str(action)}` is already registered action")
                else:
                    self.handlers['action'][action] = moduleObj.action_handlers[action]

        if moduleObj.void_react:
            if 'void' in self.handlers:
                self.handlers['void'] = moduleObj.void_react
                self.void_react = True
                message += self.tools.values.MODULE_INIT_VOID.value
            else:
                raise exceptions.LibraryRewriteError(f"[{module_name}] `{str(action)}` is already registered void")

        self.modules[module_name] = moduleObj
        self.list = module_name
        return self.tools.system_message(write = message, module = "library.uploader")
