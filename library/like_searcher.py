v = "0.6.0"
name = """Отслежка лайков"""
descr = """Уведомляет о лайках на стене сообщества."""


def init(tools):
    global plugintype
    plugintype = [
        tools.events.LIKE_ADD, 
        tools.events.LIKE_REMOVE
        ]
        

def update(tools, package):
    if package['plugintype'] in plugintype:
        response = package['plugintype']

        response += f"\n\t\tObject: {package['object_type']}{package['object_owner_id']}_{package['object_id']}"

        response += f"\n\t\t\tОт {tools.getMention(package['liker_id'], 'gen')}"
        response += f"\n\t\t\tAt {package['post_id']} {package['thread_reply_id']}"

        for i in tools.getObject("ADMIN_SUB"):
            tools.api.messages.send(
                random_id = tools.random_id(), 
                message = response, 
                peer_id = i
                )

        tools.system_message(response)
        return 1