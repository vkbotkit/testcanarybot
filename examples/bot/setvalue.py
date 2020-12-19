import testcanarybot

bot = testcanarybot.app(
    token = """:::PASTE:TOKEN:::""",
    group_id = 0
)

bot.hide('description', 'echo_bot') # hide list of selected plugins from LIBRARY_LIST

bot.setValue("ONLY_COMMANDS", False, "bool") # parsing all messages that does not starts with mention.
bot.setValue("ADD_MENTIONS", True, "bool")
bot.setMentions('каня') # custom mentions

bot.start_polling()