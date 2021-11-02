import random


v = "0.6.0"
name = """Обработчик ошибок"""
descr = """Обработчик ошибок. Реагирует "{user_name}, можешь повторить?", если бот не смог обработать команду."""

 
def init(tools):   
    global plugintype 
    plugintype = [tools.events.ERROR_HANDLER]
    tools.setObject("ERRORHANDLED_MESSAGE", ["{user}, можешь повторить?"])
    tools.setObject("ERRORHANDLED_ATTACHMENT", ["photo-195675828_457241495"])


def update(tools, package):
    if package["text"][0] == tools.getObject("NOREACT"):
        user = tools.getMention(package["from_id"], "nom")
        
        tools.api.messages.send(
            random_id = tools.random_id(), 
            peer_id = package["peer_id"], 
            message = random.choice(tools.getObject("ERRORHANDLED_MESSAGE")).format(user = user), 
            attachment = random.choice(tools.getObject("ERRORHANDLED_ATTACHMENT"))
            )

        return 1