class lib_plugin():
    def __init__(self, api, tools):
        self.v = 0.5
        self.descr = 'Print here description'
        
        self.plugintype = [
            tools.objects.MESSAGE_NEW,
            # tools.objects.LIKE_ADD,
            # tools.objects.REMOVE

            #Other types you can add via tools.setValue(itemName, value)
        ]

    # TOOLS MODULE GUIDE

    # VARIABLES:

    # tools.assets --> your folder "assets"
    # tools.objects --> all variables that you created or changed by .setObject from tools or bot
    # tools.objectslist --> list of names of objects in tools.objects. It's for tools.setObject and tools.getObject
    # tools.group_id --> identificator of your group
    # tools.shortname --> short address of your group
    # tools.group_mention --> mention of your group via @ + tools.shortname
    # tools.managers --> saved list of your managers

    # FUNCTIONS:

    # tools.add(db_name) --> add new database from assets
    # tools.get(db_name) --> get database by his name
    # tools.getDate(time = datetime.now()) --> returns date in format mm/dd/yyyy
    # tools.getTime(time = datetime.now()) --> returns time in 24 hour format
    # tools.getDateTime(time = datetime.now()) --> returns tools.getDate + tools.getTime
    # tools.system_message(textToPrint: str) --> prints your text into command line and into assets/log.txt
    # tools.random_id() --> returns integer from interval from 0 to 999999
    # tools.getMention(page_id: int, name_case = "nom") --> returns a mention. for name_case look tools.name_cases
    # tools.getManagers(group_id: int) --> get administators and owner from selected group
    # tools.isManager(from_id: int, group_id: int) --> check if it is admin of selected group
    # tools.getChatManagers(peer_id: int) --> get administators and owner from selected chat 
    # tools.getMembers(peer_id: int) --> get members of selected chat
    # tools.isMember(from_id: int, peer_id: int) --> check if it is member of this chat
    # tools.ischecktype(checklist: list, checktype: list or type object) --> check if this list have types from checktype
    # tools.setObject(nameOfObject: str, newValue) --> set object by finding him by his name
    # tools.getObject(nameOfObject: str) --> find object by his name

    # ASSETS GUIDE

    # so assets object works like open
    # for example, log file is found in tools by this way:
    # self.objects.log = self.assets("log.txt", mode = "a+", encoding = "utf-8")


    def update(self, api, tools, message):
        if message['text'][0] == 'string': # checking for string
            if message['text'][1] == tools.objects.ENDLINE: # end of line
                api.messages.send(
                    random_id = tools.random_id(), 
                    peer_id = message['peer_id'], 
                    message = 'Hello World!'
                    )
                return 1 # if you don't want to get error after sending

        elif message['text'][0] in ['list', 'of', 'strings']: # checking for list
            if message['text'][1] == tools.objects.ENDLINE: # end of line
                api.messages.send(
                    random_id = tools.random_id(), 
                    peer_id = message['peer_id'], 
                    message = 'Hello World!'
                    )
                return 1 # if you don't want to get error after sending
                        

