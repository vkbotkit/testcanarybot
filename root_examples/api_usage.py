import testcanarybot
# kensoi.github.io/testcanarybot/

bot = testcanarybot.app(
    access_token = ":::PASTE:TOKEN:::", 
    group_id = 0
    )

response = testcanarybot.init_async(
            bot.api.users.get(user_ids = 1)
        ) # вместо asyncio.get_event_loop().run_until_complete

print("{first_name} {last_name}".format(**response[0]))

mentions = ['павел', 'паша', 'павлик', 'дуров', 'дурашка']
bot.setMentions(mentions)

bot.start_polling() 

# вместо start_polling вы можете использовать check(times: int)