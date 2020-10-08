Sampleplugin for TestCanaryBot

In plugin message.text is splitted to list, int items are mentions of pages (@mention_without_spaces)

This plugin should be modified (including necessarily name of plugin project) and moved to YouBotFolder\library

Useful methods from Tools:
tools.endline = end of line
tools.managers = list of a bot managers

tools.random_id() = integer for api.messages.send (look vk.com/dev/messages.send)
tools.getMention(pageid: int, name_case: str) get [pageid|string] (@string)
tools.getManagers() = update tools.managers

name cases for getMention:
именительный – nom, 
родительный – gen,
дательный – dat, 
винительный – acc, 
творительный – ins, 
предложный – abl,
link - shortlink (to make mention like @durov)

@@@ andprokofieff.github.io
