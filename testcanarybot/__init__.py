import os
from .plugins import plugins


import traceback
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll


def getPath(file):
    return os.path.abspath(file)[:-len(file)]


class Longpoll():    
    def __init__(self, token: str, group_id: int, library: str):
        """
        Token = token you took from VK Settings: https://vk.com/{yourgroupaddress}?act=tokens
        Group_id = identificator of your group where you want to install CanaryBot Framework :)
        """
        self.bot = vk_api.VkApi(token = token)
        self.api = self.bot.get_api()
        self.supp_v = ["0.4.0"]
        
        self.longpoll = None
        self.library = plugins(self.supp_v, group_id, self.api, library)

        print(f'@{self.library.tools.shortname} started')


    def setMentions(self, *args):
        """ 
        Use custom mentions instead "@{groupadress}"
        """
        self.library.tools.setObject("MENTION", [self.library.tools.group_mention, *args])
    

    def setNameCases(self, *args):
        """Use custom mentions instead \"@{groupaddress}\""""
        self.library.tools.setObject("MENTION_NAME_CASES", args)
    
    
    def setObject(self, string: str, value):
        self.library.tools.setObject(string, value)


    def listen(self, count = None):
        """count: how many packages should take Canarybot. If you don't send this, it takes packages forever"""
        if not count:
            while True:
                self.check()

        else:
            for i in range(count):
                self.check()

            print('Done!')


    def getLongPoll(self):
        """Take longpoll"""
        return VkBotLongPoll(self.bot, str(self.library.tools.group_id))


    def check(self, debug = False):
        """Check VK for updates once time, like canarybot.listen(1)"""
        if not self.longpoll:
            self.longpoll = self.getLongPoll()
            print('Longpoll have just connected.')

        for event in self.longpoll.check():
            if not debug:
                self.library.send(event)

            else:
                try:
                    self.library.send(event)

                except Exception as e:
                    print(traceback.format_exc())
                    print(f'{e} ({Exception})')