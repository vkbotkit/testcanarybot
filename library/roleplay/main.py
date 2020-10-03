import random
class lib_plugin():
    def __init__(self):
        self.v = '002'


    def check(args):
        return 'ok'


    def update(self, api, tools, message):
        if message.text[0] in ['обнять', 'обняла', 'hug']:
            if type(message.text[1]) is int and message.text[2] == ':::CANARYBOT:endmessage:::':
                if message.text[1] == message.from_id:
                    api.messages.send(random_id = random.randint(0,9999), peer_id = message.peer_id, message=f'А себя зачем?')
                else:
                    try:
                        user = tools.getMention(message.text[1], 'acc')
                    except Exception as e:
                        print(e)
                        user = '{user}'
                    api.messages.send(random_id = random.randint(0,9999), peer_id = message.peer_id, message=f'Вы обняли {user}')

                return None
            api.messages.send(random_id = random.randint(0,9999), peer_id = message.peer_id, message=f'А кого?')
        return None
