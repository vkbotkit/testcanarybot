import random
class lib_plugin():
    def __init__(self, api, tools):
        self.v = "0.4.0"
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
                    'commands': ['отшлёпать', 'атата', 'ебануть'],
                    'name_case': 'acc',
                    'reaction': ['Вы отшлёпали {user} у всех на виду.']
                },
                {
                    'commands': ['облапать', 'общупать'],
                    'name_case': 'acc',
                    'reaction': ['Вы облапали {user} у всех на виду.', 'Вы втихушок общупали {user}.']
                },
                {
                    'commands': ['убить', 'прирезать', 'расстрелять'],
                    'name_case': 'acc',
                    'reaction': ['Вы убили {user}.']
                },
            ],
            'self': [
                {
                    'commands': ['чай', 'выпить', 'хлебнуть'],
                    'reaction': ['Вы отпили чаю.', 'Вы выпили весь чай в кружке.', 'Вы выпили весь чай в стакане.', 'Вы хлебнули чаю.']
                },
                {
                    'commands': ['кофе'],
                    'reaction': ['Вы отпили кофе.', 'Вы выпили весь кофе в кружке.', 'Вы выпили весь кофе в стакане.', 'Вы хлебнули кофе.']
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
                    'commands': ['умереть', 'сдохнуть'],
                    'reaction': ['Вы умерли.']
                },
            ],
        }


    def update(self, api, tools, message):
        for i in self.reactions['to_someone']:
            if message['text'][0] in i['commands']:
                if type(message['text'][1]) is int and message['text'][2] == tools.objects.ENDLINE:
                    if message['text'][1] == message['from_id']:
                        api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message=f'А себя зачем?')
                        return 1

                    else:
                        try:
                            user = tools.getMention(message['text'][1], i['name_case'])

                        except Exception as e:
                            tools.system_message(e)
                            user = 'user'

                        api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message=random.choice(i['reaction']).format(user = user))
                        return 1

                elif (message['text'][1] in tools.submentions.keys() or message['text'][1] in tools.submentions.values()) and message['text'][2] == tools.objects.ENDLINE:
                    api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message=random.choice(i['reaction']).format(user = message['text'][1]))
                    return 1

                elif message['text'][1] in tools.selfmention.values() and message['text'][2] == tools.objects.ENDLINE:
                    api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message=f'А себя зачем?')
                    return 1

                api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message=f'А кого?')
                return 1

        else:
            if message['text'][1] == tools.objects.ENDLINE:
                for i in self.reactions['self']:
                    if message['text'][0] in i['commands']:
                        api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message=random.choice(i['reaction']))
                        return 1
                        

