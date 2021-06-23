from testcanarybot import objects
from testcanarybot import exceptions

# Copyright 2021 kensoi

class Main(objects.libraryModule):
    @objects.priority(commands = ['quit']) # @testcanarybot quit
    async def second(self, tools: objects.tools, package: objects.package):
        raise exceptions.Quit("test") # -> to finish your framework (closing all projects that was launched by tppm)


    @objects.priority(commands = ['lib_reload']) # @testcanarybot lib_reload
    async def second2(self, tools: objects.tools, package: objects.package):
        raise exceptions.LibraryReload("Reload") # -> framework will reload your library