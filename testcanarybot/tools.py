import random
from . import objects as _objects
from datetime import datetime

class tools:
    def __init__(self, path, number, api):
        self.api = api

        self.objects = _objects
        self.objectslist = ["MENTION", "ENDLINE", "ACTION", "PAYLOAD", "NOREACT", "MESSAGE_NEW", "LIKE_ADD", "LIKE_REMOVE", "ERROR_HANDLER", "LIBRARY_SYNTAX", "CONSOLE_SYNTAX", "PARSER_SYNTAX", "LIBRARY_ERROR", "LIBRARY_NOSELECT"]
        self.assets = assets(path)

        self.group_id = number
        self.shortname = api.groups.getById(group_id=self.group_id)[0]['screen_name']
        self.group_mention = f'[club{self.group_id}|@{self.shortname}]'
        self.managers = self.getManagers(self.group_id)


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

       
    def system_message(self, text:str):
        time = datetime.now()
        date = f'{"%02d" % time.month}/{"%02d" % time.day}/{time.year} {"%02d" % time.hour}:{"%02d" % time.minute}:{"%02d" % time.second}'
        response = f'{date} @{self.shortname}.{self.plugin}: {text}'
        print(response)


    def random_id(self):
        return random.randint(0, 999999)


    def getMention(self, page:int, nc = None):
            if nc == 'link':
                if page > 0:
                    return f'[id{page}|@id{page}]'
                elif page == self.group_id:
                    return self.group_mention
                else:
                    return f'[club{-page}|@{self.api.groups.getById(group_id = -page)[0]["screen_name"]}]'
            else:
                if page > 0:
                    return f'[id{page}|{self.api.users.get(user_ids = page, name_case=nc)[0]["first_name"]}]'
                elif page == self.group_id:
                    return self.selfmention[nc]
                else:
                    return f'[club{-page}|{self.api.groups.getById(group_id = -page)[0]["name"]}]' 


    def getManagers(self, number):
        lis = self.api.groups.getMembers(group_id = number, sort = 'id_asc', filter='managers')['items']
        return [i['id'] for i in lis if i['role'] in ['administrator', 'creator']]


    def isManager(self, from_id, group_id):
        return from_id in self.getManagers(group_id)


    def getChatManagers(self, peer_id):
        res = self.api.messages.getConversationsById(peer_ids = peer_id)['items'][0]['chat_settings']
        response = [*res['admin_ids'], res['owner_id']]
        return response
        

    def isChatManager(self, from_id, peer_id):
        return from_id in self.getChatManagers(peer_id)


    def getMembers(self, peer_id):
        response = self.api.messages.getConversationMembers(peer_id = peer_id)['items']
        return [i['member_id'] for i in response]


    def isMember(self, from_id, peer_id):
        return from_id in self.getMembers(peer_id)


    def ischecktype(self, checklist, checktype):
        for i in checklist:
            if (type(i) is checktype) or (type(checktype) is list and type(i) in checktype):
                return True
            
        return False


    def setObject(self, string: str, value):
        self.objectslist.append(string)
        setattr(self.objects, string, value)

    def getObject(self, string: str):
        getattr(self.objects, string)


class assets():
    """
    lib_assets(filename, mode): open path.
    """
    def __init__(self, path):
        self.path = path


    def __call__(self, filename, mode):
        return open(self.path + filename, mode)