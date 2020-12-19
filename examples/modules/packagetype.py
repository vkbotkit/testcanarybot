from testcanarybot.objects import libraryModule
from testcanarybot.events import events

class Main(libraryModule):
    async def package_handler(self, tools, package):
        print(type(package))

    packagetype = list(events)
        
        
       


