v = 0.6
name = """Запросы SQLITE"""
descr = """{listitem} {group_mention} sql [запрос] - выполнить запрос в базу данных canarycore"""

def init(tools):
    global plugintype, descr

    plugintype = [
        tools.events.MESSAGE_NEW
    ]
    descr = descr.format(
        listitem = "{listitem}",
        group_mention = tools.group_mention
    )


def update(tools, package):
    if package['text'][0] == 'sql' and package['text'][1] != tools.getObject("ENDLINE"):
        request = " ".join(package['text'][1:-1])
        try:
            response = tools.get("canarycore").request(request)
        except:
            response = "Invalid request"
            
        response = "result: " + str(response)

        tools.api.messages.send(
            random_id = tools.random_id(), 
            peer_id = package['peer_id'], 
            message = response
            )
            
        return 1
                        

