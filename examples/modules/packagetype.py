from testcanarybot import events

class Main:
    async def start(self, tools):
        self.name = "package_type"
        self.version = "0.8.0"
        self.description = """
            testcanarybot objects type handler
            """
        self.packagetype = [
            # events.message_new
        ]
        
        
    async def package_handler(self, tools, package):
        print(type(package))
       


