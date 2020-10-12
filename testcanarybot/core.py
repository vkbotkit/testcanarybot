import random
class lib_plugin():
    def __init__(self, api, tools):
        self.v = '0.0032'
        

    def update(self, api, tools, message):
        if message['text'][0] == 'console':
            if tools.isManager(message['from_id'], tools.group_id):
                test = ' '.join(message['text'][1:-1])
                return 'console: ' + test
            else:
                user = tools.getMention(message['from_id'], 'nom')
                api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message="{user}, командная строка недоступна пользователям, не имеющих прав в сообществе {mention}".format(user = user, mention = tools.group_mention))
                return 1

        elif message['text'][0] in ['плагины', 'plugins', 'ассеты']:
            if message['text'][1] in ['описание']:
                if message['text'][2] == tools.endline:
                    api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message="Чтобы получить описание модуля, отправьте {} ассеты описание {название модуля}".format(tools.group_mention))
                    return 1
                elif type(message['text'][2]) is str and message['text'][3] == tools.endline:
                    return 'plugins: ' + message['text'][2]
            elif message['text'][1] == tools.endline:
                return 'plugins: pass'