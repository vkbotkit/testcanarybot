from testcanarybot import objects
from testcanarybot.enums import events

class Main(objects.libraryModule):
	# Заглушка для чатбота при добавлении в беседу
    async def start(self, tools: objects.tools):
        pass

    @objects.ContextManager(commands = ['пончики']) # commands
    async def ContextCommands(self, tools: objects.tools, package: objects.package):
        await tools.api.messages.send(
            random_id = tools.gen_random(),
            peer_id = package.peer_id,
            message = "А чё"
        )
        
        
    @objects.priority(commands = ['пончики2']) # commands
    async def SimilarCommands(self, tools: objects.tools, package: objects.package):
        await tools.api.messages.send(
            random_id = tools.gen_random(),
            peer_id = package.peer_id,
            message = "А чё"
        )


    @objects.ContextManager(events = [events.like_add]) # events
    async def ContextEvents(self, tools: objects.tools, package: objects.package):
        pass


    @objects.event(events = [ events.like_remove]) # events
    async def SimilarEvents(self, tools: objects.tools, package: objects.package):
        pass


    @objects.ContextManager() # void
    async def ContextVoid(self, tools: objects.tools, package: objects.package):
        pass


    @objects.void # void
    async def SimilarVoid(self, tools: objects.tools, package: objects.package):
        pass


    @objects.ContextManager(action = []) #actions like chat title edit or user kick (ONLY CHATS, eg peer_id > 2000000000) 
    async def ContextAction(self, tools: objects.tools, package: objects.package):
        pass    


    @objects.action(action = []) #actions like chat title edit or user kick (ONLY CHATS, eg peer_id > 2000000000) 
    async def SimilarAction(self, tools: objects.tools, package: objects.package):
        pass