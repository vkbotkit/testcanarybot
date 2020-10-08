import random
class lib_plugin():
    def __init__(self):
        self.v = '0.0031'
        

    def update(self, api, tools, message):
        if message.text[0] == tools.mention:
            user = tools.getMention(message.from_id, 'nom')
            api.messages.send(random_id = tools.random_id(), peer_id = message.peer_id, message="{user},".format(user = user), attachment=random.choice(self.answers['mention']))
            return 1

        elif message.text[0] == 'console':
            test = ' '.join(message.text[1:-1])
            return 'console: ' + test

        elif message.text[0] in ['плагины', 'plugins', 'ассеты']:
            if message.text[1] in ['описание']:
                if message.text[2] == tools.endline:
                    api.messages.send(random_id = tools.random_id(), peer_id = message.peer_id, message="Чтобы получить описание модуля, отправьте @canarybot ассеты описание {название модуля}")
                    return 1
                elif type(message.text[2]) is str and message.text[3] == tools.endline:
                    return 'plugins: ' + message.text[2]
            elif message.text[1] == tools.endline:
                return 'plugins: pass'

        elif message.text[0] in 'chat_invite_user':
            user = tools.getMention(message.text[1], 'nom')
            api.messages.send(random_id = tools.random_id(), peer_id = message.peer_id, message=self.answers['invite'].format(user = user))
            return 1

        elif message.text[0] in 'chat_kick_user':
            user = tools.getMention(message.text[1], 'link')
            api.messages.send(random_id = tools.random_id(), peer_id = message.peer_id, message=self.answers['kick'].format(user = user))
            return 1