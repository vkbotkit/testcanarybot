from testcanarybot import objects

class Main(objects.libraryModule):
    async def start(self, tools: objects.tools):
        self.message = """OLD TOOLS METHODS
⚡HOW TO IMPORT: from old_tools_methods import tools

⚡CONTENT:
tools.mentions_self
tools.mentions_unknown
tools.name_cases
tools.everyone
tools.getDate(time = datetime.now())
tools.getTime(time = datetime.now())
tools.getDateTime(time = datetime.now())
tools.ischecktype(checklist, checktype)

Copyright 2021 kensoi"""

    @objects.priority(commands = ["tools"])
    async def tools_info(self, tools: objects.tools, package: objects.package):
        await tools.api.messages.send(
            random_id = tools.gen_random(),
            peer_id = package.peer_id,
            message = self.message
        )
