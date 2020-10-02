import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import engine
import random


v = '001'
token = "816be56e3b314cd7af06e361b948b0f6958e87c348e1c906726c15046214f36e91bf3aad22547635c10da"


devbot = vk_api.VkApi(token = token)
longpoll = VkBotLongPoll(devbot, '195675828')
api = devbot.get_api()

plugins = engine.plugins(v, engine.assets(), api)
engine.upd_id(195675828)

print('Работа начата')

for event in longpoll.listen():
    try:
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.message.peer_id > 2000000000 and event.message.from_id == 517114114:
                parsed = engine.parse_command(event.message.text)
                api.messages.send(random_id = random.randint(0,999999), peer_id = event.message.peer_id, message = str(parsed))
    except Exception as e:
        print(e)