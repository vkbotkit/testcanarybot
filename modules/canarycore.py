import random
from testcanarybot import events
from testcanarybot.objects import static, message, expression
    # static for supporting testcanarybot 0.801 and newer
    # message to convert fwd_messages or reply_message into object

"""
System plugin to work with method error_handler in testcanarybot/library. Name "canarycore" is automaticaly hidden by system.
"""

class Main:
    library_response = "Библиотека, с которой работает {mention}:\n\n{plugins}\n\n Чтобы получить описание модуля, отправьте {mention} ассеты описание [название модуля]"
    class assets:
        class commands:
            standart = ["модули", "модуль", "modules", "module"]
            descr = ["описание", "оп", "description", "descr"]

    class parser:
        run = ["выполнить", "run"]


    async def start(self, tools):
        self.version = static
        self.name = """canarycore"""
        self.description = """Модуль для управления системой testcanarycore версии 0.6
            {group_mention} модуль [ссылка на модуль без пробелов] - показать описание модуля
            {group_mention} модули - показать библиотеку testcanarybot
            {group_mention} выполнить + [пересланные сообщения] - выполнить сообщения
            """.format(group_mention = tools.group_mention)

        self.packagetype = [
                    events.message_new
                ]


    async def package_handler(self, tools, package):
        if package.items[0] == "управление":
            return tools.getValue("LIBRARY"), "canarycore"

        elif package.items[0] in self.assets.commands.standart:
            if package.items[1] == tools.getValue("ENDLINE"):
                return tools.getValue("LIBRARY"), tools.getValue("LIBRARY_NOSELECT")

            elif package.items[2] == tools.getValue("ENDLINE"):
                return tools.getValue("LIBRARY"), package.items[1]

        elif package.items[0] in self.parser.run:
            if package.items[1] is tools.getValue("ENDLINE"):
                response = [tools.getValue("PARSER")]

                if hasattr(package, 'fwd_messages'): response.extend(message(**obj.__dict__) for obj in package.fwd_messages)
                if hasattr(package, 'reply_message'): response.append(message(**package.reply_message.__dict__))

                response.append(tools.getValue("ENDLINE"))
                return response


    async def error_handler(self, tools, package):
        if package.items[0] == tools.getValue("LIBRARY"):
            response = "response"

            if type(package.items[1]) is list: # RESPONSED A LIST OF PLUGINS FROM LIBRARY
                response_list = []
                for i in package.items[1]:
                    codename, name = i
                    response_list.append(tools.getValue("LIBRARY_RESPONSE_LIST_LINE").value.format(
                        listitem = tools.getValue("LIBRARY_RESPONSE_LIST_ITEM").value,
                        codename = codename,
                        name = name
                    ))

                response = self.library_response.format(
                        plugins = '\n'.join(response_list),
                        mention = tools.group_mention
                    )
                
                await tools.api.messages.send(
                    random_id = tools.random_id(), 
                    peer_id = package.peer_id, 
                    message = response
                    )


class simple:
    pass