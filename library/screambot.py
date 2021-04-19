import random
from testcanarybot import objects

# Copyright 2021 kensoi

# testing testcanarybot via spamming messages
# special for vk.com/screambot

class Main(objects.libraryModule):
    def __init__(self):
        objects.libraryModule.__init__(self)

        self.codename = "ScreamReact"
        self.description = """
        {listitem} @{mention} помощь - выслать инструкции в беседу
        {listitem} @{mention} генерировать [число] - сгенерировать смех в указанном количестве сообщений
        {listitem} @{mention} спам [число] - созвать всех в беседу указанном числом сообщений

        {listitem} @{mention} клички - посмотреть, на какие упоминания реагирует бот
        """
        self.mention = "@all го орать"
        self.err = "Использование: \"{mention} спам/генерировать [целое число больше 0]\""

        self.laugh_dict = "ОРУУ"
        self.rofl_dict = list("АХ")


    async def start(self, tools: objects.tools):
        self.description = self.description.format(listitem = tools.values.LISTITEM, mention = tools.getBotLink())
        self.err = self.err.format(mention = tools.getBotLink())


    def gen(self, lenght = None, choice = None):
        if not lenght: lenght = random.randint(5,256)
        if not choice: choice = bool(random.getrandbits(1))
        
        if choice:
            return self.laugh_dict[:-1] + self.laugh_dict[-1] * lenght
            
        else:
            return "".join([random.choice(self.rofl_dict) for i in range(lenght)])


    @objects.void # незарегистрированные команды или обычные сообщения
    async def scream(self, tools: objects.tools, package: objects.package):
        if set(tools.getBotMentions()) & set(package.params.mentions) != set():
            await tools.api.messages.send(
                random_id = tools.gen_random(),
                peer_id = package.peer_id,
                message = self.gen()
            )

            return None


    @objects.priority(commands = ['помощь']) # @testcanarybot помощь
    async def help(self, tools: objects.tools, package: objects.package):
        await tools.api.messages.send(
            random_id = tools.gen_random(),
            peer_id = package.peer_id,
            message = self.description
        )


    @objects.priority(commands = ['клички']) # @testcanarybot помощь
    async def helpy(self, tools: objects.tools, package: objects.package):
        await tools.api.messages.send(
            random_id = tools.gen_random(),
            peer_id = package.peer_id,
            message = ("Допустимые клички: \n{listitem} " + "\n{listitem} ".join(tools.mentions)).format(listitem = tools.values.LISTITEM)
        )


    @objects.priority(commands = ['спам', 'генерировать'])
    async def generate(self, tools: objects.tools, package: objects.package):
        counter = int(package.items[1])
        
        if counter == 0:
            await tools.api.messages.send(
                random_id = tools.gen_random(),
                peer_id = package.peer_id,
                message = self.err
            )

        else:
            if package.items[0] == 'спам':
                for count in range(counter):
                    await tools.api.messages.send(
                        random_id = tools.gen_random(),
                        peer_id = package.peer_id,
                        message = self.mention
                    )
                    
            else:
                for count in range(counter):
                    await tools.api.messages.send(
                        random_id = tools.gen_random(),
                        peer_id = package.peer_id,
                        message = self.gen()
                    )