import random

class lib_plugin():
    def __init__(self):
        self.v = '002'
        self.name = 'CANARYCORE'
        self.answers = {
            'help': {
                1: 'Ой, привет, {user}, почему ты пишешь мне?',
                2: 'Инструкция по установке: eesmth.ml/@canarybot/install \nИнструкция по чатботу: eesmth.ml/@canarybot/rules'
            },
            'link': 'Ваша ссылка: {link}'
        }

    def check(args):
        return 'ok'

    def update(self, api, tools, message):
        if message.text[0] in ['help', 'помощь', 'инструкции']:
            user = tools.getMention(message.from_id, 'nom')
            for i in self.answers['help'].values():
                api.messages.send(random_id = random.randint(0,9999), peer_id = message.peer_id, message=i.format(user = user))
            return None
        elif message.text[0] in ['short', 'link', 'сократить', 'сократи']:
            link = api.utils.getShortLink(url = ' '.join(message.text[1:-1]))['short_url']
            api.messages.send(random_id = random.randint(0,9999), peer_id = message.peer_id, message=self.answers['link'].format(link = link))

        return None


