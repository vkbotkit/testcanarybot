from testcanarybot import objects

class Main(objects.libraryModule):
    @objects.void
    async def void_handler(self, tools: objects.tools, package: objects.package):
        if package.params.command:
            await tools.api.messages.send(
                random_id = tools.random_id(),
                peer_id = package.peer_id,
                message = "void no_react"
            )

            