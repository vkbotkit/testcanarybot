import random
from testcanarybot.events import events
from testcanarybot.objects import libraryModule, message, expression


"""
System plugin to work with method error_handler in testcanarybot/library. Name "canarycore" is automaticaly hidden by system.
"""

class Main(libraryModule):
    library_response = "Библиотека, с которой работает {mention}:\n\n{plugins}\n\n Чтобы получить описание модуля, отправьте {mention} ассеты описание [название модуля]"
    class assets:
        class commands:
            standart = ["модули", "модуль", "modules", "module"]
            descr = ["описание", "оп", "description", "descr"]

    class parser:
        run = ["выполнить", "run"]


    async def start(self, tools):
        self.name = """canarycore"""
        self.description = """Модуль для управления системой testcanarybot версии 0.900
            {listitem} {group_mention}  модуль [ссылка на модуль без пробелов] - показать описание модуля
            {listitem} {group_mention}  модули - показать библиотеку testcanarybot
            {listitem} {group_mention}  выполнить + [пересланные сообщения] - выполнить сообщения
            Для выполнения команд требуется наличие прав администратора в сообществе.
            """.format(
                listitem = tools.getValue("LISTITEM"),
                group_mention = tools.group_mention
                )

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

        elif package.items[0] == 'админ':
            if await tools.isManager(package.from_id, tools.group_id):
                if package.items[1] == 'перезагрузка':
                    return tools.getValue("LIBRARY"), tools.getValue("LIBRARY_RELOAD")

            else:
                pass


    async def error_handler(self, tools, package):
        if package.items[0] == tools.getValue("LIBRARY"):
            response = "response"

            if type(package.items[1]) is list: # RESPONSED A LIST OF PLUGINS FROM LIBRARY
                response_list = []
                for i in package.items[1]:
                    codename, name = i
                    response_list.append(tools.getValue("LIBRARY_RESPONSE_LIST_LINE").value.format(
                        listitem = tools.getValue("LISTITEM").value,
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

            elif package.items[1] == tools.getValue("LIBRARY_RELOAD"):
                if package.items[2] == tools.getValue("LIBRARY_SUCCESS"):
                    await tools.api.messages.send(
                        random_id = tools.random_id(), 
                        peer_id = package.peer_id, 
                        message = "Success"
                        )



class simple:
    pass