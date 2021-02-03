from testcanarybot import objects
from testcanarybot.tools import uploader, assets
import io

class Main(objects.libraryModule):
    """
    корутина "Войд"
    все не зарегистрированные с помощью register(commands) команды будут направляться сюда.
    """

    async def start(self, tools):
        self.upload = uploader(tools.api)

    @objects.void
    async def echo(self, tools, package):
        if package.text != '':
            await tools.api.messages.send(
                random_id = tools.random_id(),
                peer_id = package.peer_id,
                message = package.text
            )
            return 1

        else:
            for att in package.attachments:
                if att.type == 'audio_message':
                    file_ogg = att.audio_message.link_ogg

                    async with tools.http.get(file_ogg) as response:
                        obj = await self.upload.audio_message(
                            audio = io.BytesIO(await response.read()),
                            peer_id = package.peer_id
                        )

                        await tools.api.messages.send(
                            random_id = tools.random_id(),
                            peer_id = package.peer_id,
                            attachment = f"audio_message{obj.audio_message.owner_id}_{obj.audio_message.id}"
                            )

                        return 1
                    


