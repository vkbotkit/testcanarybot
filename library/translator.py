import googletrans


v = "0.6.0"
name = """Google Переводчик"""
descr = """Плагин-обёртка для Google Translate. 
    Доступные языки: "{group_mention} доступные языки" 
    Перевести: "{group_mention}" переведи [язык] [текст для перевода]
    """

translator = googletrans.Translator()


def init(tools):
    global plugintype, descr, languages

    plugintype = [tools.events.MESSAGE_NEW]
    
    descr = descr.format(group_mention = tools.group_mention)

    tools.system_message('Loading languages list... ')
    test = googletrans.LANGUAGES

    tools.system_message('Appending to languages list... ')
    languages = [*test.keys()]


def update(tools, package):
    if package['text'][0] in ['tr', 'пр', 'translate', 'переведи', 'переводчик', 'translator']:
        if package['text'][1] in languages:
            if package['text'][2] == tools.getObject("ENDLINE"):
                tools.api.messages.send(
                    random_id = tools.random_id(), 
                    peer_id = package['peer_id'], 
                    message = 'Hello World!'
                    )
            
            else:
                response = ' '.join(package['text'][2:-1])
                response = translator.translate(response, dest=package['text'][1]).text
                tools.api.messages.send(
                    random_id = tools.random_id(), 
                    peer_id = package['peer_id'], 
                    message = response
                    )
                return 1
        elif package['text'][1] in ['help', 'помощь']:
            return [
                tools.getObject("LIBRARY_SYNTAX"),
                "translator.py"
            ]

        else:
            user = tools.getMention(package['from_id'], 'nom')
            response = '{user}, чтобы я перевела, отправь это: {mention} перевести [комбинация символов из доступного списка] [текст, который нужно перевести]'.format(user = user, mention = tools.group_mention)
        
            tools.api.messages.send(
                random_id = tools.random_id(), 
                peer_id = package['peer_id'], 
                message = response
                )
            return 1

    elif package['text'][0] == 'доступные' and package['text'][1] == 'языки' and package['text'][2] == tools.getObject("ENDLINE"):
        user = tools.getMention(package['from_id'], 'nom')
        response = f'{user} Вот доступный список языков: \n\n'
        response += ', '.join(languages)
        response += '\n\n{mention} перевести [комбинация символов из списка] [текст, который нужно перевести]'.format(mention = tools.group_mention)
        
        tools.api.messages.send(
            random_id = tools.random_id(), 
            peer_id = package['peer_id'], 
            message = response
            )
        return 1
