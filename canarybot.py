import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import engine
import random

def start(token: str, group_id: int):
    global devbot
    global api
    global library
        
    devbot = vk_api.VkApi(token = token)
    api = devbot.get_api()
    library = engine.plugins('003', engine.assets, engine.tools, api)
    engine.upd_id(group_id, api)
    engine.getManagers(api)

    print(f'@{engine.shortname} started')

def listen(count = None):
    if not count:
        while True:
            check()
    else:
        for i in range(10):
            check()
        print('Done!')

def check():
    longpoll = VkBotLongPoll(devbot, str(engine.group_id))

    for event in longpoll.check():
        try:
            if event.type == VkBotEventType.MESSAGE_NEW:
                    
                if event.message.action:
                    event.message.text = engine.parse_action(event.message.action)
                elif event.message.text:
                    if event.message.text != '':
                        if event.message.from_id not in engine.managers: event.message.text = event.message.text.replace('console', '')
                        event.message.text = engine.parse_command(event.message.text)
                    else: 
                        continue
                else: 
                    continue


                if event.message.text[0] != ':::CANARYBOT:endmessage:::': library.parse(event.message)
        except Exception as e:
            print(e)


# python -i canarybot.py
# start(token, group_number)