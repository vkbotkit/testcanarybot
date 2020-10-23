Sampleplugin for TestCanaryBot

In plugin message['text'] is splitted to list, int items are mentions of pages (@mention_without_spaces)

This plugin should be modified (including necessarily name of plugin project) and moved to YouBotFolder\library

Useful methods from Tools:

use it for message['text'][0]:
    tools.objects.ACTION =  if you want to manage actions (message action when message['text'] == [tools.objects.ACTION, *action.values])
    tools.objects.PAYLOAD = if you created keyboard before using vk_api (message payload when message['text'] == [tools.objects.PAYLOAD, payload dict])

tools.objects.ENDLINE = end of line
tools.managers = list of a bot managers

tools.random_id() = integer for api.messages.send (look vk.com/dev/messages.send)
tools.getMention(pageid: int, name_case: str) get [pageid|string] (@string)

tools.getManagers(group_id) = get managers list for group
tools.isManager(user_id, group_id)

tools.getMembers(peer_id) = get members of selected chat

tools.getChatManagers(peer_id) = get managers of selected chat
tools.isChatManager(user_id, peer_id) = check if selected user is manager for this chat

tools.ischecktype(list, type) check if list have values of selected type 

    tools.ischecktype(['1','2', 3], x)
    x = str => returns True in this case
    x = int => returns True in this case
    x = dict => returns False in this case

PS use tools.system_message('string') instead print() to save message.

!!!ATTENTION!!! USE ASSETS FROM FUNCTION UPDATE TO SAVE OR OPEN MEDIA
assets('filename', 'type') works like open() but it takes media from folder 'assets'


name cases for getMention:
именительный – nom, 
родительный – gen,
дательный – dat, 
винительный – acc, 
творительный – ins, 
предложный – abl,
link - shortlink (to make mention like @durov)

For now, your plugin can be supported for all TestCanaryBot versions, that supports 0.0032!
@@@ andprokofieff.github.io
