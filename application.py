import testcanarybot

devbot = testcanarybot.TestCanaryBot ("token", 0, testcanarybot.getPath(__file__)) # 0 is a group_id
devbot.setMentions('кб', 'канари', 'канарибот', 'каня', 'киоко')
devbot.listen()
# devbot.listen(1) to check for updates once.