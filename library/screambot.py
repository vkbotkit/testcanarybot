import random
from testcanarybot import objects

# Copyright 2021 kensoi
# Test module
# Special for vk.com/screambot

class Main(objects.libraryModule):
    async def start(self, tools: objects.tools):
        self.codename = "ScreamReact"
        self.description = """
        {listitem} @{mention} помощь - выслать инструкции в беседу
        {listitem} @{mention} генерировать [число] - сгенерировать смех в указанном количестве сообщений
        {listitem} @{mention} спам [число] - созвать всех в беседу указанном числом сообщений

        {listitem} @{mention} клички - посмотреть, на какие упоминания реагирует бот
        """.format(
            listitem = tools.values.LISTITEM,
            mention = tools.link
        )
        self.mention = "@all го орать"
        self.err = "Использование: \"{mention} спам/генерировать [целое число больше 0]\""

    def gen(self):   
        result = ""

        if random.randint(0,2) == 0:
            result = "ОРУ" + "У" * random.randint(5,253)
        else:
            lenght = random.randint(8, 256)

            for i in range(lenght):
                result += random.choice(['А', 'Х'])

        return result

    @objects.void # незарегистрированные команды или обычные сообщения
    async def scream(self, tools: objects.tools, package: objects.package):
        if set(tools.mentions) & set(package.params.mentions) != set():
            await tools.api.messages.send(
                random_id = tools.random_id,
                peer_id = package.peer_id,
                message = self.gen()
            )
            return None


    @objects.priority(commands = ['помощь']) # @testcanarybot помощь
    async def help(self, tools: objects.tools, package: objects.package):
        await tools.api.messages.send(
            random_id = tools.random_id,
            peer_id = package.peer_id,
            message = self.description
        )

    @objects.priority(commands = ['клички']) # @testcanarybot помощь
    async def helpy(self, tools: objects.tools, package: objects.package):
        await tools.api.messages.send(
            random_id = tools.random_id,
            peer_id = package.peer_id,
            message = ("Допустимые клички: \n{listitem} " + "\n{listitem} ".join(tools.mentions)).format(listitem = tools.values.LISTITEM)
        )

    @objects.priority(commands = ['спам', 'генерировать'])
    async def generate(self, tools: objects.tools, package: objects.package):
        counter = int(package.items[1])
        
        if counter == 0:
            await tools.api.messages.send(
                random_id = tools.random_id,
                peer_id = package.peer_id,
                message = self.err
            )

        else:
            if package.items[0] == 'спам':
                for count in range(counter):
                    await tools.api.messages.send(
                        random_id = tools.random_id,
                        peer_id = package.peer_id,
                        message = self.mention
                    )
                    
            else:
                for count in range(counter):
                    await tools.api.messages.send(
                        random_id = tools.random_id,
                        peer_id = package.peer_id,
                        message = self.gen()
                    )