import testcanarybot
# kensoi.github.io/testcanarybot/

token = """:::PASTE:TOKEN:::"""
group_id = 0

bot = testcanarybot.app(
    token = token, 
    group_id = group_id
    )


bot.start_polling()