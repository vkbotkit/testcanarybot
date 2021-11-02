v = "0.6.0"
name = """ Команды для бота:"""
descr = """{listitem} {group_mention} помощь = Отослать полезные ссылки. 
    {listitem} {group_mention} ссылка *ссылка* = Сократить ссылку с помощью VK CC 
    {listitem} {group_mention} тип *упоминание страницы, например @durov* = узнать тип страницы, её ID, краткий адрес"""
answers = {
    'help': [
        'Ой, привет, {user}, почему ты пишешь мне?',
        'Инструкция по установке: kensoi.github.io/@canarybot/install \nИнструкция по чатботу: kensoi.github.io/@canarybot/rules'
    ],
    'link': 'Ваша ссылка: {link}',
    'gettype': 'Тип страницы: {typepage} \nСсылка на страницу: {pagelink} (через ID) \nУпоминание: {mention}',
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
    if package['text'][0] in ['help', 'помощь', 'инструкции']:
        user = tools.getMention(package['from_id'], 'nom')
        for i in answers['help']:
            tools.api.messages.send(
                random_id = tools.random_id(), 
                peer_id = package['peer_id'], 
                message = i.format(user = user)
                )

        return 1

    elif package['text'][0] in ['тип', 'type', 'id', 'айди'] and type(package['text'][1]) is int:
        page_id = package['text'][1]
        mention = tools.getMention(page_id, 'link')

        page_id = f"id{page_id}" if page_id > 0 else f"club{-page_id}"
        pagelink = "https://vk.com/" + page_id
        user = tools.api.utils.resolveScreenName(screen_name = page_id)
        typepage = 'Пользователь' if user['type'] == 'user' else 'Сообщество'
        
        tools.api.messages.send(
            random_id = tools.random_id(), 
            peer_id = package['peer_id'], 
            message = answers['gettype'].format(
                typepage = typepage, 
                pagelink = pagelink, 
                mention = mention
                )
            )

        return 1

    elif package['text'][0] in ['short', 'link', 'сократить', 'сократи']:
        link = tools.api.utils.getShortLink(url = ' '.join(package['text'][1:-1]))['short_url']
        tools.api.messages.send(
            random_id = tools.random_id(), 
            peer_id = package['peer_id'], 
            message = answers['link'].format(link = link)
            )

        return 1

