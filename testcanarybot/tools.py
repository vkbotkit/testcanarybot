import random

class tools:
    def __init__(self, number, api):
        self.api = api
        self.mention = ':::CANARYBOT:MENTION:::'
        self.endline = ':::CANARYBOT:ENDMESSAGE:::'

        self.group_id = number
        self.group_mention = f'[club{self.group_id}|@canarybot]'
        self.shortname = api.groups.getById(group_id=self.group_id)[0]['screen_name']
        self.getManagers(number)
        self.selfmention = {
            'nom': 'я', 
            'gen': 'меня',
            'dat': 'мне',
            'acc': 'меня',
            'ins': 'мной',
            'abl': 'мне'
        }

        self.mentions = [self.group_mention]
        
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
        lis = self.api.groups.getMembers(group_id = self.group_id, sort = 'id_asc', filter='managers')['items']
        
        self.managers = [i['id'] for i in lis if i['role'] in ['administrator', 'creator']]


    def parse_mention(self, mentiontoparse):
        mention = mentiontoparse.replace(mentiontoparse[mentiontoparse.find('|'):], '')

        mention = mention.replace('id', '')
        mention = mention.replace('club', '-')
        mention = mention.replace('public', '-')
            
        return int(mention)


    def parse_action(self, messageaction):
        response = []
        response.extend(messageaction.values())
        response.append(self.endline)
        return response

class assets():
    """
    lib_assets(filename, mode): open path.
    """


    def __call__(self, filename, mode):
        return open(os.path.abspath(os.path.dirname(__file__)) + '\\assets\\' + filename, mode)