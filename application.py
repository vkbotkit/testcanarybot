import testcanarybot

bot = testcanarybot.Longpoll(token = """token""", group_id = 0)

bot.setMentions('your_name')
bot.setNameCases('name_cases')


bot.listen(None)