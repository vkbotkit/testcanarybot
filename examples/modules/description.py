from testcanarybot.objects import static

class Main:
    async def start(self, tools):
        self.version = static
        self.name = """canarycore"""
        self.description = """module to show description of another modules""".format(group_mention = tools.group_mention)


    async def error_handler(self, tools, package):
        if package.items[0] == tools.getValue("LIBRARY") and len(package.items) == 4:
            response = package.items[3].format(listitem = tools.getValue("LIBRARY_RESPONSE_LIST_ITEM").value)

            await tools.api.messages.send(
                random_id = tools.random_id(), 
                peer_id = package.peer_id, 
                message = response
                )
            return 1