from .. import exceptions
from .. import objects


import asyncio
import importlib
import os

join = '\\' if os.name == 'nt' else '/'

class library:
    def __init__(self, tools, library):
        self.libdir = library
        self.tools = tools
        self.private_list = []

        self.loop = asyncio.get_event_loop()


    def clear(self):
        self.list = []
        self.raw_modules = []
        
        self.modules = {}
        self.handlers = {
            'public': {
                'commands': {'all': [], 'coros': {}},
                'events': {'all': [], 'coros': {}},
                'action': {'all': [], 'coros': {}}
                # 'void': handler,
            },
            'private': {
                'commands': {'all': [], 'coros': {}},
                'events': {'all': [], 'coros': {}},
                'action': {'all': [], 'coros': {}}
                # 'void': handler,
            }
        }
            
    def reload(self):
        for i in self.raw_modules:
            importlib.reload(i)

        self.upload()


    def upload(self):
        self.clear()

        if os.path.isdir(os.getcwd() + join + self.libdir):
            listdir = os.listdir(os.getcwd() + join + self.libdir)
            listdir = [i for i in listdir if i != "__pycache__" and (i.endswith('.py') or i.count(".") == 0)]
            self.tools.log(module = "library", level = "debug", write = str(self.tools.values.LIBRARY_GET))

            if len(listdir) == 0:
                self.tools.log(module = "library", level = "error", write = self.tools.values.IMPORTERROR)
                raise ImportError(self.tools.values.IMPORTERROR)

            tasklist = [self.loop.create_task(self.upload_handler(module)) for module in listdir]

            if self.loop.is_running():
                pass
            else:
                self.loop.run_until_complete(asyncio.wait(tasklist))
                
            self.tools.log(module = "library", level = "debug", write = "Supporting event types: {event_types}".format(event_types = "\n".join(["", "\t\tevents.message_new", *["\t\t" + str(i) for i in self.handlers['private']['events']['all']], ""])))

        else:
            self.tools.log(module = "library", level = "error", write = "Module Library is not exists. Their directory should be here: " + os.getcwd() + join + self.libdir)
            raise ImportError("Module Library is not exists. Their directory should be here: " + os.getcwd() + join + self.libdir)


    async def upload_handler(self, module_name):
        module_direct = self.libdir + join + module_name
        
        if os.path.isdir(module_direct): 
            module_direct += '\\main.py'
        module_name = module_direct[:-3].replace(join, '.')
        module = importlib.import_module(module_name)
        self.raw_modules.append(module)

        if hasattr(module, 'Main'):
            moduleObj = module.Main()
            moduleObj.module_name = module_name

        else:
            self.tools.log(module = "library", level = "error", write = self.tools.values.MODULE_FAILED_NOMAIN.format(module = module_name))
            return
            
        moduleObj_set = set(dir(moduleObj))
        libraryModule = set(dir(objects.libraryModule))

        moduleObj.handlers = {
            'public': {
                'commands': {},
                'events': {},
                'action': {},
                # 'void': handler,
            },
            'private': {
                'commands': {},
                'events': {},
                'action': {},
                # 'void': handler,
            }
        }
        handlers = {
            'public': {
                'commands': {'all': [], 'coros': {}},
                'events': {'all': [], 'coros': {}},
                'action': {'all': [], 'coros': {}},
                # 'void': handler,
            },
            'private': {
                'commands': {'all': [], 'coros': {}},
                'events': {'all': [], 'coros': {}},
                'action': {'all': [], 'coros': {}},
                # 'void': handler,
            }
        }
        for coro_name in moduleObj_set - libraryModule:
            coro = getattr(moduleObj, coro_name)
            if coro_name != 'start' and callable(coro):
                try:
                    await coro()
                except Exception as e:
                    pass

        message = self.tools.values.MODULE_INIT.format(module = module_name)
        commands_count = len(moduleObj.handlers['private']['commands'].keys())
        events_count = len(moduleObj.handlers['private']['events'].keys())
        action_count = len(moduleObj.handlers['private']['action'].keys())

        if commands_count == 0 and events_count == 0 and events_count == 0 and 'action_count' not in moduleObj.handlers['private']:
            return self.tools.log(module = "library", level = "warning", write = self.tools.values.MODULE_FAILED_HANDLERS.format(module = module_name))
        
        if commands_count > 0:
            message += self.tools.values.MODULE_INIT_PRIORITY.format(count = commands_count)

            for i in moduleObj.handlers['public']['commands'].values():
                check = set(handlers['private']['commands']['all']) & set(i)
                if check != set():
                    return self.tools.log(
                        module = "library", 
                        level = "warning", 
                        write =  self.tools.values.MODULE_ALREADY.format(module = module_name, handler_type = "commands", type_list = "\n\t{listitem}".format(self.tools.values.LISTITEM).join(list(check))))

                for j in i['commands']:
                    test = "&#13;".join(j)
                    handlers['public']['commands']['all'].append(test)
                    handlers['public']['commands']['coros'][test] = i

            for i in moduleObj.handlers['private']['commands'].values():
                check = set(handlers['private']['commands']['all']) & set(i)
                if check != set():
                    return self.tools.log(
                        module = "library", 
                        level = "warning", 
                        write =  self.tools.values.MODULE_ALREADY.format(module = module_name, handler_type = "commands", type_list = "\n\t{listitem}".format(self.tools.values.LISTITEM).join(list(check))))

                for j in i['commands']:
                    test = "&#13;".join(j)
                    handlers['private']['commands']['all'].append(test)
                    handlers['private']['commands']['coros'][test] = i
                

        if events_count > 0:
            for key, value in moduleObj.handlers['public']['events'].items():
                if key in handlers['public']['events']['all']:
                    return self.tools.log(module = "library", level = "warning", write = self.tools.values.MODULE_ISALREADY.format(module = module_name, handler = str(key)))
                    
                else:
                    handlers['public']['events']['all'].append(key)
                    handlers['public']['events']['coros'][key] = value

            for key, value in moduleObj.handlers['private']['events'].items():
                if key in handlers['private']['events']['all']:
                    return self.tools.log(module = "library", level = "warning", write = self.tools.values.MODULE_ISALREADY.format(module = module_name, handler = str(key)))
                    
                else:
                    handlers['private']['events']['all'].append(key)
                    handlers['private']['events']['coros'][key] = value
        
        if action_count > 0:
            for key, value in moduleObj.handlers['public']['action'].items():
                if key in handlers['public']['action']['all']:
                    return self.tools.log(module = "library", level = "warning", write = self.tools.values.MODULE_ISALREADY.format(module = module_name, handler = str(key)))
                
                else:
                    handlers['public']['action']['all'].append(key)
                    handlers['public']['action']['coros'][key] = value

            for key, value in moduleObj.handlers['private']['action'].items():
                if key in handlers['private']['action']['all']:
                    return self.tools.log(module = "library", level = "warning", write = self.tools.values.MODULE_ISALREADY.format(module = module_name, handler = str(key)))
                
                else:
                    handlers['private']['action']['all'].append(key)
                    handlers['private']['action']['coros'][key] = value
        if 'void' in moduleObj.handlers['public']:
            if 'void' in handlers['public']:           
                return self.tools.log(module = "library", level = "warning", write = self.tools.values.MODULE_ISALREADY.format(module = module_name, handler = 'void'))
                
            else: 
                handlers['public']['void'] = moduleObj.handlers['public']['void']

        if 'void' in moduleObj.handlers['private']:
            if 'void' in handlers['private']:           
                return self.tools.log(module = "library", level = "warning", write = self.tools.values.MODULE_ISALREADY.format(module = module_name, handler = 'void'))
                
            else: 
                handlers['private']['void'] = moduleObj.handlers['private']['void']
                message += self.tools.values.MODULE_INIT_VOID

        check_commands = set(self.handlers['private']['commands']['all']) & set(handlers['private']['commands']['all'])
        check_events = set(self.handlers['private']['events']['all']) & set(handlers['private']['events']['all'])
        check_actions = set(self.handlers['private']['action']['all']) & set(handlers['private']['action']['all'])

        if check_commands != set():
            return self.tools.log(
                module = "library", 
                level = "warning", 
                write =  self.tools.values.MODULE_ALREADY.format(module = module_name, handler_type = "commands", type_list = "\n\t{listitem}".format(self.tools.values.LISTITEM).join(list(check_commands)))
            )
        elif check_events != set():
            return self.tools.log(
                module = "library", 
                level = "warning", 
                write =  self.tools.values.MODULE_ALREADY.format(module = module_name, handler_type = "events", type_list = "\n\t{listitem}".format(self.tools.values.LISTITEM).join(list(check_events)))
            )   
        elif check_actions != set():
            return self.tools.log(
                module = "library", 
                level = "warning", 
                write = self.tools.values.MODULE_ALREADY.format(module = module_name, handler_type = "actions", type_list = "\n\t{listitem}".format(self.tools.values.LISTITEM).join(list(check_actions)))
            )    
        elif 'void' in self.handlers['private'] and 'void' in handlers['private']:
            return self.tools.log(
                module = "library", 
                level = "warning", 
                write = f"[{module_name}] `void is already registered")

        else:
            self.tools.log(module = "library", level = "debug", write = self.tools.values.MODULE_VALID.format(module = module_name))

            self.handlers['public']['commands']['all'].extend(handlers['public']['commands']['all'])
            self.handlers['private']['commands']['all'].extend(handlers['private']['commands']['all'])
            self.handlers['public']['commands']['coros'].update(handlers['public']['commands']['coros'])
            self.handlers['private']['commands']['coros'].update(handlers['private']['commands']['coros'])
            self.handlers['public']['events']['all'].extend(handlers['public']['events']['all'])
            self.handlers['private']['events']['all'].extend(handlers['private']['events']['all'])
            self.handlers['public']['events']['coros'].update(handlers['public']['events']['coros'])
            self.handlers['private']['events']['coros'].update(handlers['private']['events']['coros'])
            self.handlers['public']['action']['all'].extend(handlers['public']['action']['all'])
            self.handlers['private']['action']['all'].extend(handlers['private']['action']['all'])
            self.handlers['public']['action']['coros'].update(handlers['public']['action']['coros'])
            self.handlers['private']['action']['coros'].update(handlers['private']['action']['coros'])
            if 'void' in handlers['private']:
                self.handlers['public']['void'] = handlers['public']['void']
                self.handlers['private']['void'] = handlers['private']['void']
            
            del moduleObj.handlers
            self.handlers['public']['commands']['all'].sort(key = lambda x: -x.count('&#13;'))
            self.handlers['private']['commands']['all'].sort(key = lambda x: -x.count('&#13;'))
            self.handlers['public']['commands']['coros'] = sorted(self.handlers['public']['commands']['coros'].items(), key = lambda x: -x.count('&#13;'))
            self.handlers['public']['commands']['coros'] = dict(self.handlers['public']['commands']['coros'])
            self.handlers['private']['commands']['coros'] = sorted(self.handlers['private']['commands']['coros'].items(), key = lambda x: -x.count('&#13;'))
            self.handlers['private']['commands']['coros'] = dict(self.handlers['private']['commands']['coros'])
                
            self.modules[module_name] = moduleObj
            self.list.append(module_name)
            return self.tools.log(module = "library", level = "info", write = message)
