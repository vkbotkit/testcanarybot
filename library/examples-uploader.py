from testcanarybot import objects
from testcanarybot import exceptions
from testcanarybot.uploader import Uploader
from testcanarybot.assets import assets

class Main(objects.libraryModule):
	# Заглушка для чатбота при добавлении в беседу
    async def start(self, tools):
        self.upload = Uploader(tools.api)

    @objects.ContextManager(commands = ["уплоадер"])
    async def uploaderTest(self, tools, package):
        response = await self.upload.photo_messages(photos = ["example.jpg"])
        
        await tools.api.messages.send(
            random_id = tools.gen_random(),
            peer_id = package.peer_id,
            message = "Пример с фото",
            attachment = f"photo{response[0].owner_id}_{response[0].id}"
        )
        

    @objects.ContextManager(commands = ["уплоадер2"])
    async def uploaderTest2(self, tools, package):
        response = await self.upload.document(
            document = "example.jpg", title="чё", peer_id = package.peer_id, 
        )
        
        await tools.api.messages.send(
            random_id = tools.gen_random(),
            peer_id = package.peer_id,
            message = "Пример с фото",
            attachment = f"doc{response.doc.owner_id}_{response.doc.id}"
        )

