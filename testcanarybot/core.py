import random


v = "0.6.0"
name = """Управление testcanarycore"""
descr = """Модуль для управления системой testcanarycore версии "0.6.0"
    {group_mention} плагины описание [ссылка на модуль без пробелов] - показать описание модуля
    {group_mention} плагины - показать библиотеку testcanarybot
    {group_mention} выполнить + [пересланные сообщения] - выполнить сообщения
    """


def init(tools):
    global plugintype, descr
    plugintype = [
                tools.events.MESSAGE_NEW,
                tools.events.ERROR_HANDLER
            ]
    descr = descr.format(group_mention = tools.group_mention)
    
    global assets, parser
        
    assets = tools.objects.responses()
    parser = tools.objects.responses()

    assets.commands = tools.objects.responses()

    assets.commands.standart = [
        "плагины", "плагин", "plugins", "plugin",
        "модули", "модуль", "module", "modules",
        "библиотека", "library",
        "ассеты", "ассет", "assets", "asset"
        ]
    assets.commands.descr = [ "описание", "характеристика", "оп", "description", "descr" ]
    parser.run = [ "выполнить", "run" ]
    parser.command = [ "команду", "command" ]


def update(tools, package):
    if package["plugintype"] == plugintype[0]:
        if package["text"][0] == "управление":
            return [
                tools.getObject("LIBRARY_SYNTAX"), 
                "canarycore"
            ]

        if package["text"][0] in assets.commands.standart:
            if package["text"][1] in assets.commands.descr:

                # @canarybot plugins description

                if package["text"][2] == tools.getObject("ENDLINE"):
                    tools.api.messages.send(
                        random_id = tools.random_id(), 
                        peer_id = package["peer_id"], 
                        message=tools.getObject("ASSETS_ERROR").format(
                            mention = tools.group_mention
                            )
                        )
                    return 1

                elif package["text"][3] == tools.getObject("ENDLINE"):
                    return [
                        tools.getObject("LIBRARY_SYNTAX"), 
                        package["text"][2]
                        ]
                    
            elif package["text"][1] == tools.getObject("ENDLINE"):

                # @canarybot plugins

                return [
                    tools.getObject("LIBRARY_SYNTAX"), 
                    tools.getObject("LIBRARY_NOSELECT")
                    ]

        elif package["text"][0] in parser.run and package["text"][1] in [tools.getObject("ENDLINE"), *parser.command] and package["text"][-1] is tools.getObject("ENDLINE"):
            
            # @canarybot run
            # + forwarded messages

            response = [
                tools.getObject("PARSER_SYNTAX")
                ]

            if "fwd_messages" in package: response.extend(package["fwd_messages"])
            if "reply_message" in package: response.append(package["reply_message"])

            response.append(tools.getObject("ENDLINE"))

            return response
            
    else:
        if package["text"][0] == tools.getObject("LIBRARY_SYNTAX"):
            response = "response"

            if type(package["text"][1]) is list: # RESPONSED A LIST OF PLUGINS FROM LIBRARY
                response = tools.getObject("LIBRARY_RESPONSE_LIST").format(
                        plugins = '\n'.join(
                            [tools.getObject("LIBRARY_RESPONSE_LIST_ITEM") + " " + i for i in package["text"][1]]
                            ),
                        mention = tools.group_mention
                    )

            elif package["text"][1] == tools.getObject("LIBRARY_ERROR"): # NO PLUGIN FOUND
                response = tools.getObject("LIBRARY_RESPONSE_ERROR")

            else: # RESPONSED DESCRIPTION
                response = package["text"][3].format(listitem = tools.getObject("LIBRARY_RESPONSE_LIST_ITEM"))

            tools.api.messages.send(
                random_id = tools.random_id(), 
                peer_id = package["peer_id"], 
                message = response, 
                attachment = tools.getObject("LIBRARY_PIC")
                )

        elif package["text"][0] == tools.getObject("PARSER_SYNTAX"):
            for i in package["text"][1:]:
                pass