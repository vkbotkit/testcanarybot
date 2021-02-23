from testcanarybot import objects
from testcanarybot import exceptions
from testcanarybot.keyboard import keyboard
from testcanarybot.keyboard import keyboardcolor


class Main(objects.libraryModule):
    
    async def start(self, tools):
        self.keyboardTest = keyboard(one_time = False, inline = True)

        self.keyboardTest.add_button("канари помощь", keyboardcolor.PRIMARY)
        self.keyboardTest.add_line()
        self.keyboardTest.add_button("Test1")
        self.keyboardTest.add_button("Test2")
        self.keyboardTest.add_line()
        self.keyboardTest.add_button("Test3")


    @objects.ContextManager(commands = ['клавиатура'])
    async def KeyboardTest(self, tools, package):
        await tools.api.messages.send(
            random_id = tools.random_id,
            peer_id = package.peer_id,
            message = "Пример клавиатуры",
            keyboard = self.keyboardTest.get_keyboard()
        )
