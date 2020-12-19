from testcanarybot.objects import libraryModule

class Main(libraryModule):
    async def error_handler(self, tools, package):
        if package.items[0] == tools.getValue("LIBRARY") and len(package.items) == 4:
            response = package.items[3].format(listitem = tools.getValue("LISTITEM").value)

            await tools.api.messages.send(
                random_id = tools.random_id(), 
                peer_id = package.peer_id, 
                message = response
                )
            return 1