from testcanarybot import objects

class Main(objects.libraryModule):
	# Заглушка для чатбота при добавлении в беседу
    async def start(self, tools):
        pass


    @objects.ContextManager(commands = ['ассеты'])
    async def assetsExample(self, tools, package):
        with tools.assets("readme.txt") as log: # %assets%/readme.txt
            await tools.api.messages.send(random_id = tools.gen_random(), peer_id = package.peer_id, message = log.read())
