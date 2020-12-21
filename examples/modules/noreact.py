from testcanarybot.objects import libraryModule

class Main(libraryModule):
    async def error_handler(self, tools, package):
        if tools.getValue("NOREACT") in package.items:
            tools.system_message('NO REACT MODULE EXAMPLE')
            """ here you can write reaction on not reacted message, for example:
            tools.system_message("this message is not parsed.", module = 'reacter') """
