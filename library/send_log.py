v = 0.6
name = """Отправить лог testcanarybot"""
descr = """Отправьте "{group_mention} лог", чтобы получить лог файлов. [требуется наличие прав администратора в {group_mention}]"""


def init(tools):
    global plugintype, descr
    
    plugintype = [
        tools.events.MESSAGE_NEW
    ]
    descr = descr.format(group_mention = tools.group_mention)


def update(tools, package):
    if package['text'][0] in ['log', 'лог'] and package['from_id'] in tools.managers:
        if package['text'][1] == tools.getObject("ENDLINE"):
            response = tools.upload.document_message(
                doc = tools.assets.path + "log.txt", 
                title="log.txt", 
                peer_id = package['peer_id']
            )['doc']
            response = 'doc{owner_id}_{id}'.format(**response)
            
            tools.api.messages.send(
                random_id = tools.random_id(), 
                peer_id = package['peer_id'], 
                message = 'Hello World!', 
                attachment = response
            )
            
            return 1 # if you don't want to get error after sending
                        

