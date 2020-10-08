from .plugins import plugins

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
        self.v = '0.0031'
        
        self.longpoll = None
        self.library = plugins(self.v, group_id, self.api, library)

        print(f'@{self.library.tools.shortname} started')


    def setMentions(self, *args):
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

    def check(self):
        """
        Check VK for updates once time, like canarybot.listen(1)
        """
        if not self.longpoll:
            self.longpoll = self.getLongPoll()
            print('Longpoll have just connected.')

        for event in self.longpoll.check():
            try:
                if event.type == VkBotEventType.MESSAGE_NEW:
                        
                    if event.message.action:
                        event.message.text = self.library.tools.parse_action(event.message.action)
                    elif event.message.text:
                        if event.message.text != '':
                            if event.message.from_id not in self.library.tools.managers: event.message.text = event.message.text.replace('console', '')
                            event.message.text = self.library.parse_command(event.message.text)
                        else: 
                            continue
                    else: 
                        continue


                    if event.message.text[0] != self.library.tools.endline: self.library.parse(event.message)
            
            except Exception as e:
                print(f'{e} ({Exception})')