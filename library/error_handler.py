import random

class lib_plugin():
    def __init__(self, api, tools):
        self.v = 0.5
        self.descr = 'Отладчик ошибок. Реагирует "Анон, можешь повторить?", если бот не смог обработать команду.'
        
        self.plugintype = [
            tools.objects.ERROR_HANDLER,
        ]


    def update(self, api, tools, package):
        if package["text"][0] == tools.objects.NOREACT:
            user = tools.getMention(package["from_id"], "nom")
            
            api.messages.send(
                random_id = tools.random_id(), 
                peer_id = package["peer_id"], 
                message = random.choice(tools.objects.ERRORHANDLED_MESSAGE).format(user = user), 
                attachment = random.choice(tools.objects.ERRORHANDLED_ATTACHMENT)
                )

            return 1
                        

