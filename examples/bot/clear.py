import testcanarybot
# kensoi.github.io/@testcanarybot/global.html

token = """:::PASTE:TOKEN:::"""
group_id = 0

bot = testcanarybot.app(
    token = token, 
    group_id = group_id
    )

bot.install()

bot.listen() # use method bot.installLongpoll() before this.