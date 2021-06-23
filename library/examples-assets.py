from testcanarybot import objects

# Copyright 2021 kensoi

class Main(objects.libraryModule):
    @objects.ContextManager(commands = ['ассеты'])
    async def assetsExample(self, tools, package):
        with tools.assets("readme.txt") as log: # %assets%/readme.txt
            await tools.send_reply(package, log.read())
