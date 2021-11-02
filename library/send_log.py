from vk_api.upload import VkUpload

class lib_plugin():
    def __init__(self, api, tools):
        self.v = "0.5.0"
        self.descr = 'test plugin'
        self.upload = VkUpload(api)
        # для начала назовите папку любым другим именем кроме "sampleplugin"


    def update(self, api, tools, message):
        if message['text'][0] in ['log', 'лог'] and message['from_id'] in tools.managers:
            if message['text'][1] == tools.objects.ENDLINE:
                response = self.upload.document_message(
                    doc = tools.assets.path + "log.txt", 
                    title="log.txt", 
                    peer_id = message['peer_id']
                )['doc']
                response = 'doc{owner_id}_{id}'.format(**response)
                
                api.messages.send(
                    random_id = tools.random_id(), 
                    peer_id = message['peer_id'], 
                    message = 'Hello World!', 
                    attachment = response
                )
                
                return 1 # if you don't want to get error after sending
                        

