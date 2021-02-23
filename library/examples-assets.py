from testcanarybot import objects
from testcanarybot.assets import assets

class Main(objects.libraryModule):
	# Заглушка для чатбота при добавлении в беседу
    async def start(self, tools):
        pass

    @objects.ContextManager(commands = ['ассеты'])
    async def assetsExample(self, tools, package):
        with assets("readme.txt") as log: # %assets%/readme.txt
            await tools.api.messages.send(random_id = tools.random_id, peer_id = package.peer_id, message = log.read())
