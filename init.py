import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import engine
import random


v = '002'
token = "816be56e3b314cd7af06e361b948b0f6958e87c348e1c906726c15046214f36e91bf3aad22547635c10da"


devbot = vk_api.VkApi(token = token)
longpoll = VkBotLongPoll(devbot, '195675828')
api = devbot.get_api()

library = engine.plugins(v, engine.assets(), engine.tools(api), api)
engine.upd_id(195675828, api)

print(f'@{engine.shortname} started')

for event in longpoll.listen():
    try:
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.message.peer_id > 2000000000: 
                if event.message.text == "":
                    if event.message.action:
                        event.message.text = engine.parse_action(event.message.action)
                    else:
                        continue
                else:
                    event.message.text = engine.parse_command(event.message.text)
                if event.message.text[0] != ':::CANARYBOT:endmessage:::':
                    library.parse(event.message)
    except Exception as e:
        print(e)