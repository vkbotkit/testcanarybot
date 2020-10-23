class lib_plugin():
    def __init__(self, api, tools):
        self.v = 0.4
        self.descr = "test plugin"
        self.plugintype = [tools.objects.LIKE_ADD, tools.objects.LIKE_REMOVE]
        

    def update(self, api, tools, package):
        if package['plugintype'] in self.plugintype:
            response = package['plugintype']

            like = package['text'][0]
            response += f"\n\t\tObject: {like['object_type']}{like['object_owner_id']}_{like['object_id']}"

            response += f"\n\t\t\tОт {tools.getMention(like['liker_id'], 'gen')}"
            response += f"\n\t\t\tAt {like['post_id']} {like['thread_reply_id']}"

            for i in tools.objects.ADMIN_SUB:
                api.messages.send(random_id = tools.random_id(), message = response, peer_id = i)

            tools.system_message(response)
            return 1