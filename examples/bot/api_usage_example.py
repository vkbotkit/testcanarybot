import testcanarybot

# testcanarybot 0.79
# Andrew Prokofieff 2020
# kensoi.github.io/@testcanarybot

bot = testcanarybot.app(token = ":::PASTE:TOKEN:::", group_id = 0)

response = testcanarybot.init_async(
            bot.api.users.get(user_ids = 1)
        ) # instead of asyncio.get_event_loop().run_until_complete

print(testcanarybot.supporting) # this module version supports for these plugins' versions
print("{first_name} {last_name}".format(**response[0]))

bot.setMentions('киоко')
bot.install()

bot.listen() # you can use bot.check() or bot.listen(1) if you want to check VK for events