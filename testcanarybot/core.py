import random


class lib_plugin():
    def __init__(self, api, tools):
        self.v = 0.5
        self.descr = 'test plugin'
        self.plugintype = [
            tools.objects.MESSAGE_NEW,
            tools.objects.ERROR_HANDLER
        ]
        self.assets = tools.objects.responses()
        self.parser = tools.objects.responses()
        self.errorhandl = tools.objects.responses()

        self.assets.commands = tools.objects.responses()

        self.assets.commands.standart = [
            "плагины", "плагин", "plugins", "plugin",
            "модули", "модуль", "module", "modules",
            "библиотека", "library",
            "ассеты", "ассет", "assets", "asset"
            ]
        self.assets.commands.descr = [
            "описание", "характеристика", "оп", "description", "descr"
            ]
        self.parser.run = [
            "выполнить", "run"
            ]
        self.parser.command = [
            "команду", "command"
            ]


    def update(self, api, tools, package):
        if package["plugintype"] == self.plugintype[0]:
            if package["text"][0] in self.assets.commands.standart:
                if package["text"][1] in self.assets.commands.descr:
                    if package["text"][2] == tools.objects.ENDLINE:
                        api.messages.send(
                            random_id = tools.random_id(), 
                            peer_id = package["peer_id"], 
                            message=self.tools.objects.ASSETS_ERROR.format(
                                mention = tools.group_mention
                                )
                            )
                        return 1

                    else:
                        return [tools.objects.LIBRARY_SYNTAX, " ".join(package["text"][2:-1])]
                        
                elif package["text"][1] == tools.objects.ENDLINE:
                    return [tools.objects.LIBRARY_SYNTAX, tools.objects.LIBRARY_NOSELECT]

            elif package["text"][0] in self.parser.run and package["text"][1] in [tools.objects.ENDLINE, *self.parser.command] and package["text"][-1] is tools.objects.ENDLINE:
                response = [
                    tools.objects.PARSER_SYNTAX
                    ]

                if "fwd_messages" in package: response.extend(package["fwd_messages"])
                if "reply_message" in package: response.append(package["reply_message"])

                return response

        elif package["plugintype"] == self.plugintype[1]:
            if package["text"][0] == tools.objects.LIBRARY_SYNTAX:
                response = "response"

                if type(package["text"][1]) is list: # RESPONSED A LIST OF PLUGINS FROM LIBRARY
                    response = tools.objects.LIBRARY_RESPONSE_LIST.format(
                            plugins = '\n'.join(
                                [tools.objects.LIBRARY_RESPONSE_LIST_ITEM + " " + i for i in package["text"][1]]
                                ),
                            mention = tools.group_mention
                        )

                elif package["text"][1] == tools.objects.LIBRARY_ERROR: # NO PLUGIN FOUND
                    response = tools.objects.LIBRARY_RESPONSE_ERROR

                else: # RESPONSED DESCRIPTION
                    response = tools.objects.LIBRARY_RESPONSE_DESCR.format(
                        name = package["text"][1], 
                        ver = package["text"][2], 
                        descr = package["text"][3]
                        )

                api.messages.send(
                    random_id = tools.random_id(), 
                    peer_id = package["peer_id"], 
                    message = response, 
                    attachment = tools.objects.LIBRARY_PIC
                    )

            elif package["text"][0] == tools.objects.PARSER_SYNTAX:
                for i in package["text"][1:]:
                    pass

                # парсит библиотеку