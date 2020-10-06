import random

class lib_plugin():
    def __init__(self):
        self.v = '003'
        self.answers = {
            'invite': 'Приветствую, {user}.\nПеред общением здесь ознакомься с правилами беседы и инструкциями по чатботам. \nИнструкция по Канарейке: eesmth.ml/@canarybot/rules',
            'kick': 'Кикнуть пользователя: @canarybot исключить {user}',
            'mention': [
                'video-195675828_456239018', 
                'video-195675828_456239017'
                ]
        }
        

    def update(self, api, tools, message):
        if message.text[0] == ':::CANARYBOT:mention:::':
            user = tools.getMention(message.from_id, 'nom')
            api.messages.send(random_id = random.randint(0,9999), peer_id = message.peer_id, message="{user},".format(user = user), attachment=random.choice(self.answers['mention']))
            return 1

        elif message.text[0] == 'console':
            test = ' '.join(message.text[1:-1])
            return 'console: ' + test

        elif message.text[0] in ['плагины', 'plugins', 'ассеты']:
            if message.text[1] in ['описание']:
                if message.text[2] == tools.endline:
                    api.messages.send(random_id = random.randint(0,9999), peer_id = message.peer_id, message="Чтобы получить описание модуля, отправьте @canarybot ассеты описание {название модуля}")
                    return 1
                elif type(message.text[2]) is str and message.text[3] == tools.endline:
                    return 'plugins: ' + message.text[2]
            elif message.text[1] == tools.endline:
                return 'plugins: pass'

        elif message.text[0] in 'chat_invite_user':
            user = tools.getMention(message.text[1], 'nom')
            api.messages.send(random_id = random.randint(0,9999), peer_id = message.peer_id, message=self.answers['invite'].format(user = user))
            return 1

        elif message.text[0] in 'chat_kick_user':
            user = tools.getMention(message.text[1], 'link')
            api.messages.send(random_id = random.randint(0,9999), peer_id = message.peer_id, message=self.answers['kick'].format(user = user))
            return 1