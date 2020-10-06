import random

class lib_plugin():
    def __init__(self):
        self.v = '003'
        self.descr = 'Плагин для работы с VK API и информацией о боте. \n\nКоманды для бота: \n\u2022 @canarybot помощь = Отослать полезные ссылки. \n\u2022 @canarybot ссылка *ссылка* = Сократить ссылку с помощью VK CC\n\u2022 @canarybot тип *упоминание страницы, например @durov* = узнать тип страницы, её ID, краткий адрес'
        self.answers = {
            'help': [
                'Ой, привет, {user}, почему ты пишешь мне?',
                'Инструкция по установке: eesmth.ml/@canarybot/install \nИнструкция по чатботу: eesmth.ml/@canarybot/rules'
            ],
            'link': 'Ваша ссылка: {link}',
            'gettype': 'Тип страницы: {typepage} \nСсылка на страницу: {pagelink} (через ID) \nУпоминание: {mention}',
        }
        

    def update(self, api, tools, message):
        if message.text[0] in ['help', 'помощь', 'инструкции']:
            user = tools.getMention(message.from_id, 'nom')
            for i in self.answers['help']:
                api.messages.send(random_id = random.randint(0,9999), peer_id = message.peer_id, message=i.format(user = user))
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

