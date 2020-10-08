import testcanarybot
import os

token = ''
group_id = 0
library = testcanarybot.getLibrary(__file__)
devbot = testcanarybot.TestCanaryBot (
    token, 
    group_id, library
    )
devbot.setMentions('кб', 'канари')
devbot.listen() #paste here 1 if you want to check once