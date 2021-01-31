import testcanarybot
# kensoi.github.io/testcanarybot/

token = """:::PASTE:TOKEN:::"""
group_id = 0

bot = testcanarybot.app(
    access_token = token, 
    group_id = group_id
    )

from testcanarybot.objects import package

dicttest = {
    'peer_id': 1,
    'from_id': 1,
    'items': [],
    'text': 'я люблю пончики'
}

bot.test_parse(package(**dicttest))