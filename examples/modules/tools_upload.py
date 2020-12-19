from testcanarybot.objects import libraryModule # if it supports for testcanarybot 0.7 and newer
from testcanarybot.events import events
from testcanarybot.tools import uploader, assets
import os

class Main(libraryModule):
    description = """uploader example (kensoi.github.io/testcanarybot/tools/upload.html)"""
    packagetype = [
        events.message_new
    ]
    
    async def start(self, tools): 
        self.upload = uploader(tools.api)


    async def package_handler(self, tools, package):
        if package.text.endswith('document'):
            obj = await self.upload.document(
                document = assets("log.txt", 'rb'), # testcanarybot takes assets/log.txt as logger
                title = f"@{tools.group_address} log",
                peer_id = package.peer_id
            )

            await tools.api.messages.send(
                random_id = tools.random_id(),
                peer_id = package.peer_id,
                attachment = f"doc{obj.doc.owner_id}_{obj.doc.id}")
            return 1
            
        elif package.text.endswith('audio_message'):
            try:
                info = await tools.api.messages.getConversationsById(
                    peer_ids = package.peer_id
                ) # vk.com/dev/messages.getConversationsById

                message = f"Беседу с номером {package.peer_id} основал {info.items[0].chat_settings.owner_id}" 
                    # получаем id основателя беседы, у сообществ id отрицательный
            except:
                message = f"переписка {tools.group_id} с {package.from_id}"
                    # если это переписка бота и пользователя.

            obj = await self.upload.audio_message(
                audio = assets("audio_message.ogg", 'rb'),
                peer_id = package.peer_id
            )
                # получаем объект аудиосообщения.

            message2 = str(obj.audio_message.__dict__)

            message = f"{message}\n\n\n{message2}"
            # print(message) # вывести копию сообщения в терминале

            await tools.api.messages.send(
                random_id = tools.random_id(),
                peer_id = package.peer_id,
                message = message,
                attachment = f"audio_message{obj.audio_message.owner_id}_{obj.audio_message.id}"
                )
                # отправляем сообщение с данными о беседе и аудиосообщения.
                # vk.com/dev/messages.send

            return 1

        elif package.text.endswith('photo_messages'):
            obj = await self.upload.photo_messages(photos = ["photo.png"])

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