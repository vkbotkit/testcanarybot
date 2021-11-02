import random
from . import objects
from . import databases as dbs
from datetime import datetime
import sys
import io

from vk_api.upload import VkUpload

class tools:
    def __init__(self, path, number, api):
        self.api = api

        
        self.assets = assets(path)
        self.__objects = objects
        self.log = self.assets("log.txt", "a+")
        self.events = self.__objects.events
        self.upload = VkUpload(self.api)

        print("CANARYBOT_LOG_FILE", file = self.log)
        print("TESTCANARYBOT "0.6.0"", file = self.log)
        print("BY KENSOI.GITHUB.IO 2020", file = self.log)
        print("", file = self.objects.log)
        
        self.log.flush()

        self.__db = dbs.Databases(("canarycore", path + "canarycore.db"))
        self.get = self.__db.get
        
        self.group_id = number
        self.shortname = api.groups.getById(group_id=self.group_id)[0]['screen_name']
        self.group_mention = f'[club{self.group_id}|@{self.shortname}]'
        self.managers = self.getManagers(self.group_id)

        
        self.plugin = "system"
        self.system_message(self.__objects.exp.START_LOGGER)

        self.name_cases = ['nom', 'gen', 'dat', 'acc', 'ins', 'abl']

        self.selfmention = {
            'nom': 'я', 
            'gen': 'меня',
            'gen2': 'себя',
            'dat': 'мне',
            'dat2': 'себе',
            'acc': 'меня',
            'acc2': 'себя',
            'ins': 'мной',
            'ins2': 'собой',
            'abl': 'мне',
            'abl2': 'себе',
        }
        self.submentions = {
            'all': 'всех',
            'him': 'его',
            'her': 'её',
            'it': 'это',
            'they': 'их',
            'them': 'их',
            'us': 'нас',
            'everyone': '@everyone',
            'everyone2': '@all',
            'everyone3': '@все'
        }

        self.mentions = [self.group_mention]
        self.mentions_name_cases = []


    def update_list(self):
        self.object_list = self.__objects.exp.list_of_exp


    def add(self, db_name):
        self.__db.add((db_name, self.assets.path + db_name))


    def getDate(self, time = datetime.now()):
        return f'{"%02d" % time.day}.{"%02d" % time.month}.{time.year}'
    
    
    def getTime(self, time = datetime.now()):
        return f'{"%02d" % time.hour}:{"%02d" % time.minute}:{"%02d" % time.second}'


    def getDateTime(self, time = datetime.now()):
        return self.getDate(time) + ' ' + self.getTime(time)


    def system_message(self, textToPrint:str):
        response = f'{self.getDateTime()} @{self.shortname}.{self.plugin}: \n\t{textToPrint}\n'

        print(response)
        print(response, file=self.log)

        self.log.flush()


    def random_id(self):
        return random.randint(0, 999999)


    def getMention(self, page_id: int, name_case = "nom"):
        if name_case == 'link':
            if page_id > 0:
                return f'[id{page_id}|@id{page_id}]'

            elif page_id == self.group_id:
                return self.group_mention

            else:
                return f'[club{-page_id}|@{self.api.groups.getById(group_id = -page_id)[0]["screen_name"]}]'
        
        else:
            if page_id > 0:
                request = self.api.users.get(
                    user_ids = page_id, 
                    name_case = name_case
                    )
                first_name = request[0]["first_name"]
                
                return f'[id{page_id}|{first_name}]'
            
            elif page_id == self.group_id:
                return self.selfmention[name_case]
            
            else:
                request = self.api.groups.getById(
                    group_id = -page_id
                    )
                name = request[0]["name"]
                
                return f'[club{-page_id}|{name}]' 


    def getManagers(self, group_id: int):
        lis = self.api.groups.getMembers(group_id = group_id, sort = 'id_asc', filter='managers')['items']
        return [i['id'] for i in lis if i['role'] in ['administrator', 'creator']]


    def isManager(self, from_id: int, group_id: int):
        return from_id in self.getManagers(group_id)


    def getChatManagers(self, peer_id: int):
        res = self.api.messages.getConversationsById(peer_ids = peer_id)['items'][0]['chat_settings']
        response = [*res['admin_ids'], res['owner_id']]
        return response
        

    def isChatManager(self, from_id, peer_id: int):
        return from_id in self.getChatManagers(peer_id)


    def getMembers(self, peer_id: int):
        response = self.api.messages.getConversationMembers(peer_id = peer_id)['items']
        return [i['member_id'] for i in response]


    def isMember(self, from_id: int, peer_id: int):
        return from_id in self.getMembers(peer_id)


    def ischecktype(self, checklist, checktype):
        for i in checklist:
            if isinstance(checktype, list) and type(i) in checktype:
                return True
            elif isinstance(checktype, type) and isinstance(i, checktype): 
                return True
            
        return False


    def setObject(self, nameOfObject: str, newValue):
        self.__objects.setExpression(nameOfObject, newValue)
        self.update_list()


    def getObject(self, nameOfObject: str):
        return getattr(self.__objects.exp, nameOfObject)


class assets():
    """
    assets(filename, mode, encoding): open path.
    """
    def __init__(self, path):
        self.path = path


    def __call__(self, filename, mode, encoding="utf-8"):
        return open(file = self.path + filename, mode = mode, encoding = encoding)