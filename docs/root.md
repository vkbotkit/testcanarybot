# Root parameters and methods

root example:

```python
import testcanarybot

bot = testcanarybot.app(
    accessToken = "2f206dfb5c7c4aeaff6e55e64c54ae86eb8b6e9ccab09dfa244563fd5c85277bafdac45e2bf4d06e18165",
    serviceToken = "4b982af44b982af44b982af4044bea70b544b984b982af4154d123d6075b06ad58a362a", #optional
    groupId = 195675828,

    countThread = 5
)

mentions = ['kyokou', 'kyo']
# kyokou check == @yourbot check for vk.com/yourbot
# kyo check == @yourbot check for vk.com/yourbot

bot.setMentions(mentions) # custom mentions
bot.start_polling() # infinite polling

# Another stuff:
bot.log # -> bot log with all messages
bot.api # VK API
bot.tools # tools that handlers get to parse packages
bot.testparse(package) #parse package that was created by objects.package(**dict()) 


```

