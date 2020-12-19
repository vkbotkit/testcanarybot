from testcanarybot.events import events
from testcanarybot.objects import libraryModule

class Main(libraryModule):
    async def start(self, tools):
        self.packagetype = [
            events.message_new
        ]

    async def package_handler(self, tools, package):
        if package.items[0] == 'exit' and tools.isManager(package.from_id, tools.group_id):
            quit()
        
        
