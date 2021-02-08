import threading
import asyncio
import json

from . import objects
from . import exceptions
from .enums import events, action


class handler(threading.Thread):
    processing = False

    def __init__(self, library, handler_id):
        threading.Thread.__init__(self)
        self.daemon = True
        self.handler_id = handler_id

        self.library = library
        self.packages = []


    def run(self):
        self.setName(f"handler_{self.handler_id}")
        self.library.tools.system_message(f"{self.getName()} is started", module = "package_handler")

        self.all_messages = self.library.tools.values.ALL_MESSAGES.value
        self.add_mentions = self.library.tools.values.MENTIONS.value
        self.mentions = self.library.tools.mentions

        self.thread_loop = asyncio.new_event_loop()
        self.thread_loop.set_exception_handler(self.exception_handler)
        asyncio.set_event_loop(self.thread_loop)
        self.library.tools.http.create_session(self)

        self.thread_loop.run_forever()

    def exception_handler(self, loop, context):
        try:
            raise context['exception']

        except exceptions.CallVoid as e:
            for i in self.library.handlers['void']:
                module = self.library.modules[i.__module__]

                peer_id, from_id = str(e)[1:].split("_")
                package = objects.package(**{
                    'peer_id': int(peer_id), 
                    'from_id': int(from_id), 
                    'items': [self.library.tools.values.NOREPLY]
                    })
                task = self.thread_loop.create_task(i(module, self.library.tools, package))

        except Exception as e:
            print(type(context['exception']).__name__)
            print(e)

    def create_task(self, package):
        if isinstance(package, objects.package):
            if package.type == events.message_new or package.type in self.library.handlers['events']:
                asyncio.run_coroutine_threadsafe(self.resolver(package), self.thread_loop)

        else:
            asyncio.run_coroutine_threadsafe(self.__start_module(package), self.thread_loop)

    async def __start_module(self, package):
        self.thread_loop.create_task(package(self.library.tools))

    async def resolver(self, package):
        if package.type == events.message_new:
            package.params.action = False
            package.params.payload = False

            if hasattr(package, 'action'): 
                package.params.action = True
                package.action.type = getattr(action, package.action.type)

            elif hasattr(package, 'payload'): 
                package.params.payload = True
                package.payload = json.loads(package.params)
            
            elif package.text != '':
                message = package.text.split()
                package.params.command = False
                if len(message) > 1 and ((message[0].lower() in self.mentions) or (message[0][:-1].lower() in self.mentions)):
                    package.params.gment = message.pop(0)
                    package.params.command = True

                package = await self.findMentions(package, message)

            elif len(package.attachments) > 0: 
                package.params.attachments = True

            await self.handler(package)
            
        else:
            await self.handler(package)


    async def findMentions(self, package: objects.package, message: str) -> objects.package:
        for count in range(len(message)):
            if message[count][0] == '[' and message[count].count('|') == 1:
                if message[count].count(']') > 0:
                    mention = self.library.tools.parse_mention(
                            message[count][message[count].rfind('[') + 1:message[count].find(']')]
                            )
                    package.params.mentions.append(mention)
                    package.items.append(
                        mention
                        )
                else:
                    for j in range(count, len(message)):
                        if message[j].count(']') > 0:
                            last_string, message[j] = message[j][0:message[j].find(']')], message[j][message[j].find(']') + 1:]
                            mention = self.library.tools.parse_mention(" ".join([*message[count:j], last_string])[1:])
                            package.items.append(mention)
                            package.params.mentions.append(mention)
                            count = j
                            break
            else:
                package.items.append(message[count])
            count += 1
        return package
            

    async def handler(self, package: objects.package):
        package.items.append(self.library.tools.values.ENDLINE)
        try:
            if package.type == events.message_new:
                test = objects.WaitReply(package)

                if test in self.library.tools.waiting_replies:
                    self.library.tools.waiting_replies[test] = package

                elif package.params.action:
                    for i in self.library.action_handlers[package.action.type]:
                        module = self.library.modules[i.__module__]
                        
                        self.thread_loop.create_task(i(module, self.library.tools, package))

                elif package.params.command and len(package.items) > 0 and package.items[0] in self.library.handlers['priority'].keys():
                    for i in self.library.handlers['priority'][package.items[0]]:
                        module = self.library.modules[i.__module__]
                        
                        self.thread_loop.create_task(i(module, self.library.tools, package))

                elif self.library.void_react:
                    if self.all_messages or package.params.command:
                        for i in self.library.handlers['void']:
                            module = self.library.modules[i.__module__]

                            self.thread_loop.create_task(i(module, self.library.tools, package))

            elif package.type in self.library.handlers['events'].keys():
                for i in self.library.handlers['events'][package.type]:
                    module = self.library.modules[i.__module__]
                    self.thread_loop.create_task(i(module, self.library.tools, package))

        except Exception as e:
            self.library.tools.system_message(module = "exception_handler", write = e)
