from .. import exceptions
from .. import objects


import asyncio
import importlib
import os
import sys

class library:
    def __init__(self, tools, library):
        self.libdir = library
        self.tools = tools

        self.loop = asyncio.get_event_loop()


    def clear(self):
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
            
    def reload(self):
        for i in self.raw_modules:
            importlib.reload(i)

        self.upload()


    def upload(self):
        self.clear()

        if os.path.isdir(os.getcwd() + '\\' + self.libdir):
            listdir = os.listdir(os.getcwd() + '\\' + self.libdir)
            listdir = [i for i in listdir if i != "__pycache__" and (i.endswith('.py') or i.count(".") == 0)]
            self.tools.system_message(module = "library", level = "debug", write = str(self.tools.values.LIBRARY_GET))

            if len(listdir) == 0:
                self.tools.system_message(module = "library", level = "error", write = self.tools.values.IMPORTERROR)
                raise ImportError(self.tools.values.IMPORTERROR)

            tasklist = [self.loop.create_task(self.upload_handler(module)) for module in listdir]

            if self.loop.is_running():
                pass
            else:
                self.loop.run_until_complete(asyncio.wait(tasklist))
                
            self.tools.system_message(module = "library", level = "debug", write = "Supporting event types: {event_types}".format(event_types = "\n".join(["", "\t\tevents.message_new", *["\t\t" + str(i) for i in self.handlers['events'].keys()], ""])))

        else:
            self.tools.system_message(module = "library", level = "error", write = "Module Library is not exists. Their directory should be here: " + os.getcwd() + '\\' + self.libdir)
            raise ImportError("Module Library is not exists. Their directory should be here: " + os.getcwd() + '\\' + self.libdir)


    async def upload_handler(self, module_name):
        module_direct = self.libdir + '\\' + module_name
        
        if os.path.isdir(module_direct): 
            module_direct += '\\main.py'
        module_name = module_direct[:-3].replace('\\', '.')
        module = importlib.import_module(module_name)
        self.raw_modules.append(module)

        if hasattr(module, 'Main'):
            moduleObj = module.Main()
            moduleObj.module_name = module_name
                    
            if not issubclass(type(moduleObj), objects.libraryModule):
                self.tools.system_message(module = "library", level = "error", write = self.tools.values.MODULE_FAILED_SUBCLASS.value.format(module = module_name))
                return

        else:
            self.tools.system_message(module = "library", level = "error", write = self.tools.values.MODULE_FAILED_BROKEN.format(module = module_name))
            return
            
        moduleObj_set = dir(moduleObj)
        moduleObj_set = set(moduleObj_set)

        libraryModule = dir(objects.libraryModule)
        libraryModule = set(libraryModule)

        moduleObj.event_handlers = {}
        moduleObj.commands = []
        moduleObj.action_handlers = {}
        for coro_name in moduleObj_set - libraryModule:
            coro = getattr(moduleObj, coro_name)

            if coro_name != 'start' and callable(coro):
                try:
                    await coro()
                except:
                    pass


        message = self.tools.values.MODULE_INIT.format(module = module_name)
        commands_count = len(moduleObj.commands)
        events_count = len(moduleObj.event_handlers.keys())
        action_count = len(moduleObj.action_handlers.keys())


        if commands_count == 0 and events_count == 0 and not moduleObj.void_react:
            return self.tools.system_message(module = "library", level = "error", write = self.tools.values.MODULE_FAILED_HANDLERS.format(module = module_name))
        
        if commands_count > 0:
            message += self.tools.values.MODULE_INIT_PRIORITY.format(count = commands_count)

            for i in moduleObj.handler_dict.values():
                for j in i['commands']:
                    if j in self.handlers['priority']:
                        self.tools.system_message(module = "library", level = "error", write = f"[{module_name}] `{str(j)}` is already registered command")
                        raise exceptions.LibraryRewriteError(f"[{module_name}] `{str(j)}` is already registered command")

                    else:
                        self.handlers['priority'][j] = i['handler']

        if events_count > 0:
            for event in moduleObj.event_handlers.keys():
                message += self.tools.values.MODULE_INIT_EVENTS.format(event = str(event))
                if event in self.handlers['events']:
                    self.tools.system_message(module = "library", level = "error", write = f"[{module_name}] `{str(event)}` is already registered event")
                    raise exceptions.LibraryRewriteError(f"[{module_name}] `{str(event)}` is already registered event")

                else:
                    self.handlers['events'][event] = moduleObj.event_handlers[event]
        
        if action_count > 0:
            for action in moduleObj.action_handlers.keys():
                message += self.tools.values.MODULE_INIT_ACTION.format(action = str(action))

                if action in self.handlers['action']:
                    self.tools.system_message(module = "library", level = "error", write = f"[{module_name}] `{str(action)}` is already registered action")
                    raise exceptions.LibraryRewriteError(f"[{module_name}] `{str(action)}` is already registered action")

                else:
                    self.handlers['action'][action] = moduleObj.action_handlers[action]

        if moduleObj.void_react:
            if not self.void_react:
                self.void_react = True
                self.handlers['void'] = moduleObj.void_react
                message += self.tools.values.MODULE_INIT_VOID

            else:
                self.tools.system_message(module = "library", level = "error", write = f"[{module_name}] `void is already registered")
                raise exceptions.LibraryRewriteError(f"[{module_name}] `void is already registered")

        self.modules[module_name] = moduleObj
        self.list.append(module_name)
        self.tools.system_message(module = "library", level = "DEBUG", write = message)
        return 
