import threading
import asyncio
import json
import traceback
import re
import os
import sys

from .. import objects
from .. import exceptions
from ..enums import events, action


class thread(threading.Thread):
    def __init__(self, library, handler_id, cache):
        threading.Thread.__init__(self)

        self.daemon = True

        self.library = library
        self.handler_id = handler_id
        self.cache = cache
        self.start()


    def run(self):
        thread_name = f"{self.cache}_{self.handler_id}"
        self.setName(thread_name)

        self.thread_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.thread_loop)

        self.test_handler = packageHandler(self.library)
        self.test_handler.library.tools.http.create_session(self)

        self.test_handler.library.tools.log(module = "framework", level = "debug", write = f"{self.getName()} is started")
        self.thread_loop.run_forever()


    def create_task(self, package):
        if hasattr(self, "thread_loop"):
            pass
        else:
            self.thread_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.thread_loop)

        if isinstance(package, objects.package):
            events = self.supportingEvents()

            if package.type in events:
                asyncio.run_coroutine_threadsafe(self.test_handler.resolver(package), self.thread_loop)

        else:
            asyncio.run_coroutine_threadsafe(self.__start_module(package), self.thread_loop)

    async def __start_module(self, package):
        self.thread_loop.create_task(package(self.test_handler.library.tools))


class packageHandler:
    def __init__(self, library):
        self.library = library
        self.thread_loop = asyncio.get_event_loop()
        self.thread_loop.set_exception_handler(self.exception_handler)
        self.all_messages = self.library.tools.values.ALL_MESSAGES

        if self.all_messages:
            self.am = set([*self.mentions, *self.library.tools.values.ADDITIONAL_MENTIONS])
        self.add_mentions = self.library.tools.values.ADD_MENTIONS
        self.mentions = self.library.tools.getBotMentions()
        self.packages = []

        self.define_key = "@" + self.library.tools.getBotLink() + ":"
        self.define_botment = objects.mention(self.library.tools.getBotId(), self.library.tools.getBotLink())


    def supportingEvents(self):
        response = []
        response.append(events.message_new)
        response.extend(self.library.handlers['private']['events']['all'])

        return response


    def exception_handler(self, loop, context):
        typed = type(context['exception'])
        reason = str(context['exception'])

        if typed == exceptions.Quit:
            self.library.tools.log(module = "framework", level = "debug", write = "Quited with message: " + reason)
            
            os._exit(1)

        elif typed == exceptions.LibraryReload:
            self.library.reload()

            for i in self.library.modules.values():
                if hasattr(i, "start"): 
                    self.thread_loop.create_task(i.start)

            self.library.tools.log(module = "framework", level = "debug", write = "Reloaded with message: " + reason)

        elif typed == exceptions.CallVoid:
            if 'void' not in self.library['private']:
                if reason[0] == "$" and reason.count("_") == 1:
                    peer_id, from_id = reason[1:].split("_")
                    
                    if from_id in self.library.private_list:
                        handler = self.library.handlers['private']['void']['coro']
                        module = self.library.handlers['private']['void']['libraryModule']

                    elif 'void' in self.library.handler['public']:
                        handler = self.library.handlers['public']['void']['coro']
                        module = self.library.handlers['public']['void']['libraryModule']
                    
                    else:
                        self.library.tools.log(
                            module = "framework",
                            level = "debug",
                            write = "Attempted to call void with incorrect task: " + reason
                        )

                    package = objects.package({
                        'peer_id': int(peer_id), 
                        'from_id': int(from_id), 
                        'items': [self.library.tools.values.NOREPLY]
                        })
                    package.params.command = True

                    self.thread_loop.create_task(handler(module, self.library.tools, package))

                else:
                    self.library.tools.log(
                        module = "framework",
                        level = "debug",
                        write = "Attempted to call void with incorrect task: " + reason
                    )

            else: 
                self.library.tools.log(
                        module = "framework",
                        level = "debug",
                        write = "Attempted to call void with incorrect task: " + reason
                    )

        else:
            self.library.tools.log(module = "traceback", level = "debug", write = traceback.format_exc())
            self.library.tools.log(module = "framework", level = "error", write = "Appeared exception: " + reason)


    async def resolver(self, package):
        try:
            if package.type == events.message_new:
                package.params.action = False
                package.params.payload = False

                if hasattr(package, 'action'): 
                    package.params.action = True
                    package.action.type = getattr(action, package.action.type)

                elif hasattr(package, 'payload'): 
                    package.params.payload = True
                    package.payload = json.loads(package.payload)
                
                elif package.text != '':
                    bot_ment = None
                    mentions = re.findall(r'\[(.*?)\]', package.text)
                    text_copy = package.text + ""

                    package.params.command = False
                    package.params.bot_mentioned = False
                    package.params.mentions = []
                    

                    for i in range(len(mentions)):
                        text_copy = text_copy.replace(mentions[i], self.define_key + str(i), 1)
                        page_id = mentions[i][0: mentions[i].find('|')]
                        page_id = page_id.replace('id', '', 1)
                        page_id = page_id.replace('club', '-', 1)
                        page_id = page_id.replace('public', '-', 1)

                        call = mentions[i][mentions[i].find('|') + 1:]

                        response = objects.mention(int(page_id), call)
                        package.params.mentions.append(response)

                    
                    message = text_copy.split()

                    package.items = message

                    for item in range(len(package.items)):
                        if package.items[item][package.items[item].find("[") + 1: package.items[item].rfind("]")].startswith(self.define_key):
                            package.items[item] = package.items[item][package.items[item].find("[") + 1: package.items[item].rfind("]")]
                            package.items[item] = package.items[item].replace(self.define_key, "")
                            package.items[item] = int(package.items[item])
                            package.items[item] = package.params.mentions[package.items[item]]


                    if len(message) > 1:
                        check = type(message[0])
                        if check == str:
                            check_command = message[0].lower()
                            if re.search("|".join(self.mentions), check_command):
                                package.params.gment = message.pop(0)
                                package.params.command = True

                        elif check == objects.mention:
                            if message[0].id == self.define_botment.id:
                                package.params.gment = message.pop(0)
                                package.params.command = True

                    if len(package.params.mentions) > 0:
                        if package.params.mentions[0] == bot_ment:
                            package.params.mentions.pop(0)
                            
                    if self.add_mentions:
                        mentionslisted = list(map(int, package.params.mentions))
                        k = set(map(lambda x: str(x).lower(), package.items))
                        
                        if self.define_botment.id in mentionslisted:
                            package.params.bot_mentioned = True

                        elif k & self.am != set():
                            package.params.bot_mentioned = True



                elif len(package.attachments) > 0: 
                    package.params.attachments = True


            await self.handler(package)
        except Exception as e:
            print(traceback.format_exc())
            print(e)


    async def handler(self, package: objects.package):
        try:
            package.items.append(self.library.tools.values.ENDLINE)

            if self.library.tools.wait_check(package):
                task = objects.task(package)
                self.library.tools._tools__waiting_replies[task] = package
                return

            access_type='private' if package.from_id in self.library.private_list else 'public'

            if package.type == events.message_new:
                if package.params.action:
                    if package.action.type in self.library.handlers[access_type]['action']['all']:
                        module = self.library.handlers[access_type]['actions']['coros'][package.action.type]['libraryModule']
                        handler = self.library.handlers[access_type]['actions']['coros'][package.action.type]['handler']
                        task = self.thread_loop.create_task(handler(module, self.library.tools, package))
                        return
                
                if package.params.command and len(package.items) > 0:
                    for i in self.library.handlers[access_type]['commands']['all']:
                        res = [*(i.split("&#13;")), '$items']
                        if package.check(res) or package.check(i.split("&#13;")):
                            module = self.library.handlers[access_type]['commands']['coros'][i]['libraryModule']
                            handler = self.library.handlers[access_type]['commands']['coros'][i]['handler']
                            task = self.thread_loop.create_task(handler(module, self.library.tools, package))
                            return
                
                if 'void' in self.library.handlers[access_type]:
                    if self.all_messages or package.params.command or package.params.bot_mentioned:
                        module = self.library.handlers[access_type]['void']['libraryModule']
                        handler = self.library.handlers[access_type]['void']['handler']
                        task = self.thread_loop.create_task(handler(module, self.library.tools, package))
                        return
            elif package.type in self.library.handlers[access_type]['events']['all']:
                module = self.library.handlers[access_type]['events']['coros'][package.type]['libraryModule']
                handler = self.library.handlers[access_type]['events']['coros'][package.type]['handler']
                task = self.thread_loop.create_task(handler(module, self.library.tools, package))
                return

        except Exception as e:
            self.library.tools.log(module = "traceback", level = "debug", write = traceback.format_exc())
            self.library.tools.log(module = "framework", level = "warning", write = "Appeared exception: " + str(e))


    def create_task(self, package):
        if isinstance(package, objects.package):
            events = self.supportingEvents()

            if package.type in events:
                self.thread_loop.create_task(self.resolver(package))

        else:
            self.thread_loop.create_task(self.__start_module(package))

    async def __start_module(self, package):
        await package(self.library.tools)