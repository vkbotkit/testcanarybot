from .plugins import plugins

import traceback
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

class TestCanaryBot():    
    def __init__(self, token: str, group_id: int, library: str):
        """
        Token = token you took from VK Settings: https://vk.com/{yourgroupaddress}?act=tokens
        Group_id = identificator of your group where you want to install CanaryBot Framework :)
        """
        self.bot = vk_api.VkApi(token = token)
        self.api = self.bot.get_api()
        self.supp_v = ['0.0032']
        
        self.longpoll = None
        self.library = plugins(self.supp_v, group_id, self.api, library)

        print(f'@{self.library.tools.shortname} started')


    def setMentions(self, *args):
        """ 
        Use custom mentions instead "@{groupadress}"
        """
        self.library.tools.mentions = [self.library.tools.group_mention, *args]

    def listen(self, count = None):
        """ 
        count: how many packages should take Canarybot. If you don't send this, it takes packages forever
        """

        if not count:
            while True:
                self.check()
        else:
            for i in range(count):
                self.check()

            print('Done!')


    def getLongPoll(self):
        """
        Take longpoll
        """
        return VkBotLongPoll(self.bot, str(self.library.tools.group_id))


    def parse(self, event):
        try:
            if event.type == VkBotEventType.MESSAGE_NEW:
                message = event.object['message']
                if 'action' in message:
                    message['text'] = self.library.parse_action(message['action'])
                elif 'payload' in message:
                    message['text'] = self.library.parse_payload(message['payload'])
                elif 'text' in message:
                    if message['text'] != '':
                        if message['from_id'] not in self.library.tools.managers: message['text'] = message['text'].replace('console', '')
                        message['text'] = self.library.parse_command(message['text'])
                    else: 
                        return None
                else: 
                    return None


                if message['text'][0] != self.library.tools.endline: self.library.parse(message)
        
        except Exception as e:
            print(traceback.format_exc())
            print(f'{e} ({Exception})')


    def check(self):
        """
        Check VK for updates once time, like canarybot.listen(1)
        """
        if not self.longpoll:
            self.longpoll = self.getLongPoll()
            print('Longpoll have just connected.')

        for event in self.longpoll.check():
            self.parse(event)