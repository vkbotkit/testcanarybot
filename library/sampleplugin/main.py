class lib_plugin():
    def __init__(self, api, tools):
        self.v = '0.3.2'
        self.descr = 'Шаблонный плагин для версии ' + self.v
        # для начала назовите папку любым другим именем кроме "sampleplugin"


    def update(self, api, tools, message):
        if message['text'][0] == 'test':
            if message['text'][1] == tools.endline:
                api.messages.send(random_id = tools.random_id(), peer_id = message['peer_id'], message = 'Hello World!')
                return 1 # if you don't want to get error after sending
                        

