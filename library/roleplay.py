import random


v = 0.6
name = """Roleplay"""
descrcover = """Плагин для проведения ролевых игр."""
cmdcover = """\n{listitem} {group_mention} {cmd_type} {mention_type}"""

reactions = {
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

def init(tools):
    global plugintype, descr

    plugintype = [
        tools.events.MESSAGE_NEW
    ]
    descr = descrcover

    descr += "\n"
    for i in reactions['to_someone']:
        descr += cmdcover.format(
            listitem = "{listitem}",
            group_mention = tools.group_mention,
            cmd_type = i['commands'][0],
            mention_type = "[упоминание одного человека]"
        )

    descr += "\n"
    for i in reactions['self']:
        descr += cmdcover.format(
            listitem = "{listitem}",
            group_mention = tools.group_mention,
            cmd_type = i['commands'][0],
            mention_type = ""
        )

def update(tools, message):
    for i in reactions['to_someone']:
        if message['text'][0] in i['commands']:
            if type(message['text'][1]) is int and message['text'][2] == tools.getObject("ENDLINE"):
                if message['text'][1] == message['from_id']:
                    tools.api.messages.send(
                        random_id = tools.random_id(), 
                        peer_id = message['peer_id'], 
                        message = f'А себя зачем?'
                        )

                    return 1

                else:
                    try:
                        user = tools.getMention(message['text'][1], i['name_case'])

                    except Exception as e:
                        tools.system_message(e)
                        user = 'user'

                    tools.api.messages.send(
                        random_id = tools.random_id(), 
                        peer_id = message['peer_id'], 
                        message = random.choice(i['reaction']).format(user = user)
                        )

                    return 1

            elif (message['text'][1] in tools.submentions.keys() or message['text'][1] in tools.submentions.values()) and message['text'][2] == tools.getObject("ENDLINE"):
                tools.api.messages.send(
                    random_id = tools.random_id(), 
                    peer_id = message['peer_id'], 
                    message = random.choice(i['reaction']).format(user = message['text'][1])
                    )

                return 1

            elif message['text'][1] in tools.selfmention.values() and message['text'][2] == tools.getObject("ENDLINE"):
                tools.api.messages.send(
                    random_id = tools.random_id(), 
                    peer_id = message['peer_id'], 
                    message = f'А себя зачем?'
                    )

                return 1

            tools.api.messages.send(
                random_id = tools.random_id(), 
                peer_id = message['peer_id'], 
                message = f'А кого?'
                )

            return 1

        if message['text'][0] == 'рп' and message['text'][1] == 'помощь':
            print('test')
            return [
                tools.getObject("LIBRARY_SYNTAX"), 
                "roleplay.py"
                ]

        if message['text'][1] == tools.getObject("ENDLINE"):
            for i in reactions['self']:
                if message['text'][0] in i['commands']:
                    tools.api.messages.send(
                        random_id = tools.random_id(), 
                        peer_id = message['peer_id'], 
                        message = random.choice(i['reaction'])
                        )
                        
                    return 1
                        

