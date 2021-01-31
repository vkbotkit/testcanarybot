from testcanarybot import objects
from testcanarybot.enums import events

class Main(objects.libraryModule):
    @objects.event(events = [events.like_add, events.like_remove])
    async def like_handler(self, tools: objects.tools, package: objects.package):
        pass