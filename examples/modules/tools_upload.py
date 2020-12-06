from testcanarybot.objects import static # if it supports for testcanarybot 0.7 and newer
from testcanarybot.tools import uploader
from testcanarybot import events

class Main(object):
    async def start(self, tools): 
        self.name = """uploader example (kensoi.github.io/testcanarybot/tools/upload.html)"""
        self.version = static
        self.description = """description"""
        self.packagetype = [
            events.MESSAGE_NEW
        ]
        self.upload = uploader(tools.api)


    async def package_handler(self, tools, package):
        if package.text.endswith('document'):
            obj = await self.upload.document(
                doc = tools.log, # testcanarybot takes assets/log.txt as logger
                title = f"@{tools.group_address} log",
                peer_id = package.peer_id
            )

            await tools.api.messages.send(
                random_id = tools.random_id(),
                peer_id = package.peer_id,
                attachment = ",".join(
                [f"doc{i.doc.owner_id}_{i.doc.id}" for i in obj]
                )
            )
            return 1
            
        elif package.text.endswith('audio_message'):
            obj = await self.upload.audio_message(
                audio = "audio_message.ogg",
                peer_id = package.peer_id
            )

            await tools.api.messages.send(
                random_id = tools.random_id(),
                peer_id = package.peer_id,
                attachment = f"audio_message{obj.audio_message.owner_id}_{obj.audio_message.id}"
                )

            return 1

        elif package.text.endswith('photo_messages'):
            obj = list()
            ph = ["photo.png"]
            obj.append(await self.upload.photo_messages(photos = ph))

            await tools.api.messages.send(
                random_id = tools.random_id(),
                peer_id = package.peer_id,
                attachment = ",".join(
                [f"photo{i.owner_id}_{i.id}" for i in obj]
                )
            )
            return 1

        elif package.text.endswith('photo_chat'):
            try:
                await self.upload.photo_chat(
                    photo = 'photo.png',
                    peer_id = package.peer_id
                )

            except ValueError as e:
                tools.system_message(f'Unable to make request ({e})')
                await tools.api.messages.send(
                    random_id = tools.random_id(),
                    peer_id = package.peer_id,
                    message = f'Unable to make request ({e})'
                )
                
            finally:
                return 1


        elif package.text.endswith('story'):
            obj = await self.upload.story(
                file = "GRAF_1592247712984.png",
                file_type = "photo", 
                link_text="ыыыыыы",
                link_url="https://vk.com/testcanarybot"
            )

            listoff = ",".join([f"story{i.owner_id}_{i.id}_{i.access_key}" for i in obj.items])
            
            await tools.api.messages.send(
                random_id = tools.random_id(),
                peer_id = package.peer_id,
                attachment = listoff
            )
            return 1