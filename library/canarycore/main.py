import random

class lib_plugin():
    def __init__(self):
        self.v = '002'
        self.answers = {
            'help': {
                1: 'Ой, привет, {user}, почему ты пишешь мне?',
                2: 'Инструкция по установке: eesmth.ml/@canarybot/install \nИнструкция по чатботу: eesmth.ml/@canarybot/rules'
            },
            'invite': 'Приветствую, {user}.\nПеред общением здесь ознакомься с правилами беседы и инструкциями по чатботам. \nИнструкция по Канарейке: eesmth.ml/@canarybot/rules',
            'kick': 'Кикнуть пользователя: @canarybot исключить {user}',
            'link': 'Ваша ссылка: {link}',
            'gettype': 'Тип страницы: {typepage} \nСсылка на страницу: {pagelink} (через ID) \nУпоминание: {mention}'
        }

    def check(args):
        return 'ok'

    def update(self, api, tools, message):
        if message.text[0] == ':::CANARYBOT:mention:::':
            user = tools.getMention(message.from_id, 'nom')
            api.messages.send(random_id = random.randint(0,9999), peer_id = message.peer_id, message="{user},".format(user = user), attachment='video-195675828_456239017')
            return 1

        elif message.text[0] in ['help', 'помощь', 'инструкции']:
            user = tools.getMention(message.from_id, 'nom')
            for i in self.answers['help'].values():
                api.messages.send(random_id = random.randint(0,9999), peer_id = message.peer_id, message=i.format(user = user))
            return 1

        elif message.text[0] in ['chat_invite_user']:
            user = tools.getMention(message.text[1], 'nom')
            api.messages.send(random_id = random.randint(0,9999), peer_id = message.peer_id, message=self.answers['invite'].format(user = user))
            return 1

        elif message.text[0] in ['chat_kick_user']:
            user = tools.getMention(message.text[1], 'link')
            api.messages.send(random_id = random.randint(0,9999), peer_id = message.peer_id, message=self.answers['kick'].format(user = user))
            return 1

        elif message.text[0] in ['тип', 'type', 'id', 'айди'] and type(message.text[1]) is int:
            page_id = message.text[1]
            mention = tools.getMention(page_id, 'link')

            page_id = f"id{page_id}" if page_id > 0 else f"club{-page_id}"
            pagelink = "https://vk.com/" + page_id
            user = api.utils.resolveScreenName(screen_name = page_id)
            typepage = 'Пользователь' if user['type'] == 'user' else 'Сообщество'
            
            api.messages.send(random_id = random.randint(0,9999), peer_id = message.peer_id, message=self.answers['gettype'].format(typepage=typepage,pagelink=pagelink, mention=mention))
            return 1

        elif message.text[0] in ['short', 'link', 'сократить', 'сократи']:
            link = api.utils.getShortLink(url = ' '.join(message.text[1:-1]))['short_url']
            api.messages.send(random_id = random.randint(0,9999), peer_id = message.peer_id, message=self.answers['link'].format(link = link))
            return 1


