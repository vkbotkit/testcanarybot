import random
import vk_api.exceptions
class lib_plugin():
    def __init__(self, api, tools):
        self.v = 0.4
        self.descr = 'Модуль для работы с message.action и упоминаниями бота'
        self.mentions = ['video-195675828_456239017', 'video-195675828_456239018']

        
        self.help: [
            'Ой, привет, {user}, добро пожаловать в беседу!',
            'Инструкция по чатботу: eesmth.ml/@canarybot/rules'
        ]
        self.invite = {
            'self_admin': 'Святые булочки! {user} вернулся!',
            'self_user': 'Привет, {user}! Чтобы начать работать со мной, отправь "{mention} помощь"',
        }
        self.kick = {
            'self_admin': 'Админ вышел из чата. Помянем.',
            'self_user': 'Пользователь вышел из чата. Исключить: "{mention} исключить {user}"',
            'damn': ['Зачем ты так с ним?..']
        }


    def update(self, api, tools, message):
        if message['text'][0] == tools.objects.MENTION:
            user = tools.getMention(message['from_id'], 'nom')
            api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message="{user},".format(user = user), attachment=random.choice(self.mentions))
            return 1

        elif message['text'][0] == tools.objects.ACTION:
            if message['text'][1] == 'chat_invite_user':
                if message['text'][2] == message['from_id']:
                    if tools.isChatManager(message['text'][2], message['peer_id']):
                        response = self.invite['self_admin']
                    else:
                        response = self.invite['self_user']

                    user = tools.getMention(message['text'][2], 'nom')
                    response = response.format(mention = tools.group_mention, user = user)
                    api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message=response)
                    
                elif message['text'][2] == tools.group_id:
                    response = self.help
                    for i in response:
                        api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message=i.format(mention = tools.group_mention, user = user))
                return 1


            elif message['text'][1] == 'chat_kick_user':
                if message['text'][2] == message['from_id']:
                    if tools.isChatManager(message['text'][2], message['peer_id']):
                        response = self.kick['self_admin']
                    else:
                        response = self.kick['self_user']
                else:
                    response = random.choice(self.kick['damn'])

                user = tools.getMention(message['text'][2], 'link')
                response = response.format(mention = tools.group_mention, user = user)
                
                api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message=response)
                return 1

        elif message['text'][0] == tools.objects.PAYLOAD and type(message['text'][1]) is dict:
            api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message=message['text'][1], attachment=self.invite['attachment'])
            return 1

        elif message['text'][0] in ['kick', 'кик', 'исключить']:
            if message['peer_id'] == message['from_id']:
                user = tools.getMention(message['from_id'], 'nom')
                response = '{user}, невозможно исключать пользователей не в беседе.'

                api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message = response)
            
            elif tools.isChatManager(message['from_id'], message['peer_id']):
                test = message['text'][1:-1]
                if 'fwd_messages' in message: test.extend([i['from_id'] for i in message['fwd_messages']])
                if 'reply_message' in message: test.append(message['reply_message']['from_id'])

                user = tools.getMention(message['from_id'], 'nom')

                if tools.ischecktype(test, int):
                    for i in test:
                        if type(i) is int and i != message['from_id']:
                            try:
                                api.messages.removeChatUser(chat_id = message['peer_id'] - 2000000000, member_id = i)
                                
                            except vk_api.exceptions.VkApiError as e:
                                response = 'Не получилось исключить пользователя: '

                                if tools.isChatManager(i, message['peer_id']):
                                    response += 'у человека есть права в чате.'

                                elif not tools.isMember(i, message['peer_id']):
                                    response += 'пользователя нет в чате.'

                                tools.system_message(message['peer_id'] + ":" + response)
                                api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message = response)
                            iskicked = True
                    
                    return 1
            else:
                user = tools.getMention(message['from_id'], 'nom')
                response = '{user}, не получилось исключить пользователей: у вас нет прав.'
                api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message = response)
                return 1
