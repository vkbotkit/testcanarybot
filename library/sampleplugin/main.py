v = "0.6.0"
name = """testcanarybot plugin"""
descr = """plugin descr"""

def init(tools):
    global plugintype
    
    plugintype = [
        tools.events.MESSAGE_NEW,
        # tools.events.LIKE_ADD,
        # tools.events.REMOVE

        # list of all types you can find via tools.events.list_of_types
    ]

    # TOOLS MODULE GUIDE

    # VARIABLES:

    # tools.api --> vkontakte API, for methods look vk.com/dev/methods
    # tools.upload --> uploader, look example at send_log.py
    # tools.assets(file_name, file_mode, encoding = "utf-8") --> opens files from your folder "assets". similar to open
    # tools.events = list of event types
    # tools.object_list --> list of names of objects. You can you use it to check all values through tools.getObject(name, value)
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
    # for example, log file you can open by this method:
    # tools.assets("log.txt", mode = "r+", encoding = "utf-8")


    def update(tools, package):
        if package['text'][0] == 'string': # checking for string
            if package['text'][1] == tools.objects.ENDLINE: # end of line
                tools.api.messages.send(
                    random_id = tools.random_id(), 
                    peer_id = package['peer_id'], 
                    message = 'Hello World!'
                    )
                return 1 # if you don't want to get error after sending

        elif package['text'][0] in ['list', 'of', 'strings']: # checking for list
            if package['text'][1] == tools.objects.ENDLINE: # end of line
                tools.api.messages.send(
                    random_id = tools.random_id(), 
                    peer_id = package['peer_id'], 
                    message = 'Hello World!'
                    )
                return 1 # if you don't want to get error after sending
                        

