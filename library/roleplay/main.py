import random
class lib_plugin():
    def __init__(self, api, tools):
        self.v = '0.3.2'
        self.descr = 'Плагин для проведения ролевых игр.'
        self.reactions = {
            'to_someone': [
                {
                    'commands': ['обнять', 'обняла', 'обняли'],
                    'name_case': 'acc',
                    'reaction': ['Вы обняли {user}.']
                },
                {
                    'commands': ['поцеловать', 'поцеловали', 'чмок', 'чмаф', 'цмок', 'цом'],
                    'name_case': 'acc',
                    'reaction': ['Вы поцеловали {user}.']
                },
                {
                    'commands': ['убить', 'прирезать', 'расстрелять'],
                    'name_case': 'acc',
                    'reaction': ['Вы убили {user}.']
                },
                {
                    'commands': ['изнасиловать', 'трахнуть', 'выебать'],
                    'name_case': 'acc',
                    'reaction': ['Вы принудили {user} к непотребству.', 'Вы принудили {user} к сексу.', 'Вы принудили {user} к размножению.']
                },
            ],
            'self': [
                {
                    'commands': ['чай', 'выпить', 'хлебнуть'],
                    'reaction': ['Вы отпили чаю.', 'Вы выпили чаю.', 'Вы хлебнули чаю.']
                },
                {
                    'commands': ['лежать', 'лечь', 'упасть'],
                    'reaction': ['Вы легли.', 'Вы лежите.']
                },
                {
                    'commands': ['вздохнуть', 'вздох', 'ех'],
                    'reaction': ['Вы вздохнули.']
                },
                {
                    'commands': ['умереть', 'сдох'],
                    'reaction': ['Вы умерли.']
                },
            ],
        }


    def update(self, api, tools, message):
        for i in self.reactions['to_someone']:
            if message['text'][0] in i['commands']:
                if type(message['text'][1]) is int and message['text'][2] == tools.endline:
                    if message['text'][1] == message['from_id']:
                        api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message=f'А себя зачем?')
                        return 1
                    else:
                        try:
                            user = tools.getMention(message['text'][1], i['name_case'])
                        except Exception as e:
                            print(e)
                            user = 'user'
                        api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message=random.choice(i['reaction']).format(user = user))
                        return 1

                api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message=f'А кого?')
                return 1
        else:
            if message['text'][1] == tools.endline:
                for i in self.reactions['self']:
                    if message['text'][0] in i['commands']:
                        api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message=random.choice(i['reaction']))
                        return 1
                        

