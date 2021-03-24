# Root parameters and methods

root example:
```python
'''

This is raw created root file for testcanarybot project.
fill all important info and try to run with "$ python testcanarybot --run [LIST OF PROJECT DIRECTORIES]"

'''
import os
import testcanarybot

community_name = 'Канарейка-чан'     #optional
community_token = '2f206dfb5c7c4aeaff6e55e64c54ae86eb8b6e9ccab09dfa244563fd5c85277bafdac45e2bf4d06e18165'
community_id = 195675828


community_service = '4b982af44b982af44b982af4044bea70b544b984b982af4154d123d6075b06ad58a362a'  # optional
apiVersion = '5.130'    # optional
countThread = 10        # optional

mentions = ['канари', 'каня', 'canarybot', 'canary']
ALL_MESSAGES = False
ADD_MENTIONS = False
LISTITEM = '*'

LOGLEVEL = "INFO"       # CRITICAL/ERROR/WARNING/INFO/DEBUG/NOTSET


if __name__ == '__main__':
    if os.path.abspath(__file__)[:len(os.getcwd())] == os.getcwd():
        pass
    else:
        os.chdir(__file__[:__file__.rfind("/")])
    
    bot = testcanarybot.app(
        accessToken = community_token,
        groupId = community_id,
        serviceToken = community_service, apiVersion = apiVersion, countThread = countThread, level = LOGLEVEL)
    bot.setMentions(mentions)

    bot.tools.values.set("ALL_MESSAGES", ALL_MESSAGES)
    bot.tools.values.set("ADD_MENTIONS", ADD_MENTIONS)
    bot.tools.values.set("LISTITEM", LISTITEM)

    bot.start_polling()
```