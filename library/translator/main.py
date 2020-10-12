import googletrans

class lib_plugin():
    def __init__(self, api, tools):
        self.v = '0.0032'
        self.descr = 'Переводчик'
        self.translator = googletrans.Translator()
        
        tools.system_message('Loading languages list... ')
        test = googletrans.LANGUAGES

        tools.system_message('Appending to languages list... ')
        self.languages = [*test.keys()]


    def update(self, api, tools, message):
        if message['text'][0] in ['tr', 'пр', 'translate', 'переведи', 'переводчик', 'translator']:
            if message['text'][1] in self.languages:
                if message['text'][2] == tools.endline:
                    api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message = 'Hello World!')
                else:
                    response = ' '.join(message['text'][2:-1])
                    response = self.translator.translate(response, dest=message['text'][1])['text']
                    
                    api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message = response)
                
                    return 1
            else:
                user = tools.getMention(message['from_id'], 'nom')
                response = '{user}, чтобы я перевела, отправь это: {mention} перевести [комбинация символов из доступного списка] [текст, который нужно перевести]'.format(user = user, mention = tools.group_mention)
            
                api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message = response)
                return 1
        elif message['text'][0] == 'доступные' and message['text'][1] == 'языки' and message['text'][2] == tools.endline:
            user = tools.getMention(message['from_id'], 'nom')
            response = f'{user} Вот доступный список языков: \n\n'
            response += ', '.join(self.languages)
            response += '\n\n{mention} перевести [комбинация символов из списка] [текст, который нужно перевести]'.format(mention = tools.group_mention)
            
            api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message = response)
            return 1
