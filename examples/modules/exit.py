from testcanarybot import events
from testcanarybot.objects import static

class Main:
    async def start(self, tools):
        self.name = "exit"
        self.version = static
        self.description = """
            Test plugin
            """
        self.packagetype = [
            events.MESSAGE_NEW
        ]

    async def package_handler(self, tools, package):
        if package.items[0] == '1':
            quit()
        
        
