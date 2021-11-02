class lib_plugin():
    def __init__(self, api, tools):
        self.v = "0.5.0"
        self.descr = 'test plugin'


    def update(self, api, tools, message):
        if message['text'][0] == 'sql' and message['text'][1] != tools.objects.ENDLINE:
            request = " ".join(message['text'][1:-1])
            try:
                response = tools.get("canarycore").request(request)
            except:
                response = "Invalid request"
                
            api.messages.send(
                random_id = tools.random_id(), 
                peer_id = message['peer_id'], 
                message = response
                )
                
            return 1
                        

