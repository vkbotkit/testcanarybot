from testcanarybot import objects
from testcanarybot import exceptions


class Main(objects.libraryModule):
    @objects.priority(commands = ["помощь"])
    async def help_handler(self, tools: objects.tools, package: objects.package):
        """
        корутина "приоритет"
        все команды, которые начинаются с "помощь" будут автоматически направляться сюда
        """
        await tools.api.messages.send(
            random_id = tools.random_id(),
            peer_id = package.peer_id,
            message = "Команда, которая направляет на помощь"
        )


    @objects.priority(commands = ['реплитест'])
    async def reply_test(self, tools, package):
        await tools.api.messages.send(
            random_id = tools.random_id(),
            peer_id = package.peer_id,
            message = "анкета"
        )


        package = await tools.wait_reply(package) # ожидать сообщение из этого чата.
        await tools.api.messages.send(
            random_id = tools.random_id(),
            peer_id = package.peer_id,
            message = "анкета 2"
        )


    @objects.priority(commands = ["выход"])
    async def package_handler(self, tools: objects.tools, package: objects.package):
        if tools.isManager(package.from_id, tools.group_id):
            quit()
            
        else:
            raise exceptions.CallVoid # вызов войд функций
