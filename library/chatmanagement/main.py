import random


v = "0.6.0"
name = """Чат-менеджер"""
descr = """Управление беседой
{group_mention} кик [список упоминаний/присланные сообщения] - исключить пользователей
"""

mentions = ['video-195675828_456239017', 'video-195675828_456239018']

cmd_help = [
    'Ой, привет, {user}, добро пожаловать в беседу!',
    'Инструкция по чатботу: eesmth.ml/@canarybot/rules'
]
invite = {
    'self_admin': 'Святые булочки! {user} вернулся!',
    'self_user': 'Привет, {user}! Чтобы начать работать со мной, отправь "{mention} помощь"',
}
kick = {
    'self_admin': 'Админ вышел из чата. Помянем.',
    'self_user': 'Пользователь вышел из чата. Исключить: "{mention} исключить {user}"',
    'damn': ['Зачем ты так с ним?..']
}


def init(tools):
    global plugintype, descr
    plugintype = [
        tools.events.MESSAGE_NEW
    ]
    
    descr = descr.format(
        group_mention = tools.group_mention,
        listitem = "{listitem}"
    )


def update(tools, package):
    if package['text'][0] == tools.getObject("MENTION"):
        user = tools.getMention(package['from_id'], 'nom')
        tools.api.messages.send(
            random_id = tools.random_id(), 
            peer_id = package['peer_id'], 
            message = "{user},".format(user = user), 
            attachment=random.choice(mentions)
            )
        return 1

    elif package['text'][0] == tools.getObject("ACTION"):
        if package['text'][1] == 'chat_invite_user':
            if package['text'][2] == package['from_id']:
                if tools.isChatManager(package['text'][2], package['peer_id']):
                    response = invite['self_admin']
                else:
                    response = invite['self_user']

                user = tools.getMention(package['text'][2], 'nom')
                response = response.format(
                    mention = tools.group_mention, 
                    user = user
                    )

                api.messages.send(
                    random_id = tools.random_id(), 
                    peer_id = package['peer_id'], 
                    message = response
                    )
                
            elif package['text'][2] == tools.group_id:
                response = cmd_help
                for i in response:
                    api.messages.send(
                        random_id = tools.random_id(), 
                        peer_id = package['peer_id'], 
                        message = i.format(
                            mention = tools.group_mention, 
                            user = user
                            )
                        )

            return 1

        elif package['text'][1] == 'chat_kick_user':
            if package['text'][2] == package['from_id']:
                if tools.isChatManager(package['text'][2], package['peer_id']):
                    response = kick['self_admin']
                else:
                    response = kick['self_user']
            else:
                response = random.choice(kick['damn'])

            user = tools.getMention(package['text'][2], 'link')
            response = response.format(mention = tools.group_mention, user = user)
            
            api.messages.send(
                random_id = tools.random_id(), 
                peer_id = package['peer_id'], 
                message = response
                )

            return 1

    elif package['text'][0] == tools.getObject("PAYLOAD") and type(package['text'][1]) is dict:
        api.messages.send(
            random_id = tools.random_id(), 
            peer_id = package['peer_id'], 
            message = package['text'][1], 
            attachment = invite['attachment']
            )

        return 1

    elif package['text'][0] in ['kick', 'кик', 'исключить']:
        if package['peer_id'] == package['from_id']:
            user = tools.getMention(package['from_id'], 'nom')
            response = '{user}, невозможно исключать пользователей не в беседе.'

            api.messages.send(
                random_id = tools.random_id(), 
                peer_id = package['peer_id'], 
                message = response
                )
        
        elif tools.isChatManager(package['from_id'], package['peer_id']):
            test = package['text'][1:-1]
            if 'fwd_messages' in package: test.extend([i['from_id'] for i in package['fwd_messages']])
            if 'reply_message' in package: test.append(package['reply_message']['from_id'])

            user = tools.getMention(package['from_id'], 'nom')

            if tools.ischecktype(test, int):
                for i in test:
                    if type(i) is int and i != package['from_id']:
                        try:
                            api.messages.removeChatUser(
                                chat_id = message['peer_id'] - 2000000000, 
                                member_id = i
                                )
                            
                        except:
                            response = 'Не получилось исключить пользователя: '

                            if tools.isChatManager(i, package['peer_id']):
                                response += 'у человека есть права в чате.'

                            elif not tools.isMember(i, package['peer_id']):
                                response += 'пользователя нет в чате.'

                            tools.system_message(package['peer_id'] + ":" + response)

                            tools.api.messages.send(
                                random_id = tools.random_id(), 
                                peer_id = package['peer_id'], 
                                message = response
                                )
                        iskicked = True
                
                return 1
        else:
            user = tools.getMention(package['from_id'], 'nom')
            response = '{user}, не получилось исключить пользователей: у вас нет прав.'
            api.messages.send(
                random_id = tools.random_id(), 
                peer_id = package['peer_id'], 
                message = response
                )
            return 1
