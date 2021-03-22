from testcanarybot import objects
from testcanarybot import exceptions
from testcanarybot.keyboard import keyboard
from testcanarybot.keyboard import keyboardcolor


class Main(objects.libraryModule):
    
    async def start(self, tools):
        self.keyboardTest = keyboard(one_time = False, inline = True)
        self.keyboardTest2 = keyboard(one_time = False, inline = True)

        self.keyboardTest.add_button("канари помощь", keyboardcolor.PRIMARY)
        self.keyboardTest.add_line()
        self.keyboardTest.add_button("Test1")
        self.keyboardTest.add_button("Test2")
        self.keyboardTest.add_line()
        self.keyboardTest.add_button("Test3")

        
        self.keyboardTest2.add_button("тесто", keyboardcolor.PRIMARY)
        self.keyboardTest2.add_line()
        self.keyboardTest2.add_location_button()
        


    @objects.ContextManager(commands = ['клавиатура'])
    async def KeyboardTest(self, tools, package):
        await tools.api.messages.send(
            random_id = tools.random_id,
            peer_id = package.peer_id,
            message = "Пример клавиатуры",
            keyboard = self.keyboardTest.get_keyboard()
        )

    @objects.ContextManager(commands = ['клавиатура2'])
    async def KeyboardTest2(self, tools, package):
        await tools.api.messages.send(
            random_id = tools.random_id,
            peer_id = package.peer_id,
            message = "Пример клавиатуры",
            keyboard = self.keyboardTest2.get_keyboard()
        )
        while True:
            test = await tools.wait_reply(package)
            await tools.api.messages.send(
                random_id = tools.random_id,
                peer_id = package.peer_id,
                message = "Кнопка сработала", 
            )
            