from testcanarybot import objects
from testcanarybot import exceptions
from testcanarybot.uploader import Uploader

# Copyright 2021 kensoi

class Main(objects.libraryModule):
    async def start(self, tools):
        self.upload = Uploader(tools)

    @objects.ContextManager(commands = ["уплоадер"])
    async def uploaderTest(self, tools, package):
        response = await self.upload.photo_messages(photos = ["example.jpg"])
        await tools.send_attachment(package, f"photo{response[0].owner_id}_{response[0].id}")
        

    @objects.ContextManager(commands = ["уплоадер2"])
    async def uploaderTest2(self, tools, package):
        response = await self.upload.document(document = "example.jpg", title="чё", peer_id = package.peer_id)
        await tools.send_attachment(package, f"doc{response.doc.owner_id}_{response.doc.id}")

