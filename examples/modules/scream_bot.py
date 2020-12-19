from testcanarybot.objects import libraryModule
from testcanarybot.events import events
import random

"""
testcanarybot example on vk.com/screambot
"""

class Main(libraryModule):
    tomention = "@all го орать"
    async def start(self, tools): 
        self.name = """Реакции @screambot"""
        self.description = """
        {listitem} @screambot помощь - выслать инструкции в беседу
        {listitem} @screambot генерировать [число] - сгенерировать смех в указанном количестве сообщений
        {listitem} @screambot спам [число] - созвать всех в беседу указанном числом сообщений
        Примечание: бот реагирует на любое сообщение, содержащее в себе "ору" вне учёта регистра
        """ 
        
        self.packagetype = [
            events.message_new,
        ]


    def gen(self):   
        result = ""

        if random.randint(0,2) == 0:
            result = "ору" + "у" * random.randint(5,253)
        else:
            lenght = random.randint(8, 256)

            for i in range(lenght):
                result += random.choice(['а', 'х'])

        if random.randint(0,2) == 0:
            result = result.upper()

        return result


    async def package_handler(self, tools, package):
        if package.items[0] == tools.getValue("MENTION"):
            await tools.api.messages.send(
                random_id = tools.random_id(),
                peer_id = package.peer_id,
                message = self.gen()
            )
            return None

        elif package.items == ['помощь']:
            return tools.getValue("LIBRARY"), "scream_bot"

        elif isinstance(package.items[1], str) and package.items[2] is tools.getValue("ENDLINE"):
            try:
                counter = int(package.items[1])
                if package.items[0] == 'спам':
                    for count in range(counter):
                        await tools.api.messages.send(
                            random_id = tools.random_id(),
                            peer_id = package.peer_id,
                            message = self.tomention
                        )
                elif package.items[0] == 'генерировать':
                    for count in range(counter):
                        await tools.api.messages.send(
                            random_id = tools.random_id(),
                            peer_id = package.peer_id,
                            message = self.gen()
                        )
                else:
                    raise TypeError(package.items[0])

            except ValueError as e:
                await tools.api.messages.send(
                            random_id = tools.random_id(),
                            peer_id = package.peer_id,
                            message = f"Не получилось определить значение, попробуйте снова. Ошибка: \"{e}\""
                        )
                return None

            except TypeError as e:
                await tools.api.messages.send(
                            random_id = tools.random_id(),
                            peer_id = package.peer_id,
                            message = f"Неизвестная команда. Ошибка: \"{e}\""
                        )
                return None

        else:
            for i in tools.getValue("MENTIONS").value:
                if i in package.text:
                    await tools.api.messages.send(
                        random_id = tools.random_id(),
                        peer_id = package.peer_id,
                        message = self.gen()
                    )
                    return None


