# Корневой файл проекта (root.py)

Пример корня:
```python
'''
testcanarybot project root
Copyright 2021 kensoi

This is raw created root file for testcanarybot project.
fill all important info and try to run with "$ python testcanarybot --run [LIST OF PROJECT DIRECTORIES]"

'''

import testcanarybot

community_name = 'Канарейка чан'
community_token = 'ABCDEF' # https://vk.com/yourbot?act=tokens
community_id = 0

community_service = 'ABCDEF' # to make requests via standalone application (TAKE FROM https://vk.com/editapp?id=YOURAPPID&section=options)
apiVersion = '5.130'    # optional
countThread = 10        # optional

MENTIONS = []
ADDITIONAL_MENTIONS = []
PRIVATELIST = [] # for private events
ALL_MESSAGES = False
ADD_MENTIONS = False
LISTITEM = '*'

PRINT_LOG = False
LOGLEVEL = "INFO"       # CRITICAL/ERROR/WARNING/INFO/DEBUG/NOTSET

assets = 'assets'
library = 'library'



if testcanarybot.root_init(__name__, __file__): # False -> it was launched through tppm
    bot = testcanarybot.app(
        accessToken = community_token,
        groupId = community_id,
        serviceToken = community_service, apiVersion = apiVersion, countThread = countThread, print_log=PRINT_LOG, level = LOGLEVEL)

    bot.setMentions(MENTIONS)
    bot.setPrivateList(PRIVATELIST)

    bot.tools.values.set("ALL_MESSAGES", ALL_MESSAGES)
    bot.tools.values.set("ADD_MENTIONS", ADD_MENTIONS)
    bot.tools.values.set("LISTITEM", LISTITEM)
    bot.tools.values.set('ADDITIONAL_MENTIONS', ADDITIONAL_MENTIONS)

    bot.start_polling()
```