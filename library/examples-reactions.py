from testcanarybot import objects
from testcanarybot.enums import events

class Main(objects.libraryModule):
	# Заглушка для чатбота при добавлении в беседу
    async def start(self, tools: objects.tools):
        pass

    @objects.ContextManager(commands = ['пончики']) # commands
    async def testContext(self, tools: objects.tools, package: objects.package):
        await tools.api.messages.send(
            random_id = tools.random_id,
            peer_id = package.peer_id,
            message = "А чё"
        )

    @objects.ContextManager(events = [events.like_add, events.like_remove]) # events
    async def testContext2(self, tools: objects.tools, package: objects.package):
        pass

    @objects.ContextManager() # void
    async def testContext3(self, tools: objects.tools, package: objects.package):
        pass

    @objects.ContextManager(action = []) #actions like chat title edit or user kick (ONLY CHATS, eg peer_id > 2000000000) 
    async def testContext4(self, tools: objects.tools, package: objects.package):
        pass