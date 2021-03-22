import random
from testcanarybot import objects
from testcanarybot import exceptions

class Main(objects.libraryModule):
    async def start(self, tools: objects.tools):
        pass


    @objects.priority(commands = ['quit']) # @testcanarybot quit
    async def second2(self, tools: objects.tools, package: objects.package):
        await tools.api.messages.send(
            random_id = tools.random_id,
            peer_id = package.peer_id,
            message = 'выхожу из фреймворка...'
        )
        raise exceptions.Quit("test") # -> to finish your framework (closing all projects that was runned by packaet)

    @objects.priority(commands = ['lib_reload']) # @testcanarybot lib_reload
    async def second2(self, tools: objects.tools, package: objects.package):
        await tools.api.messages.send(
            random_id = tools.random_id,
            peer_id = package.peer_id,
            message = 'старт перезагрузки...'
        )
        raise exceptions.LibraryReload("Reload") # -> framework will reload your library