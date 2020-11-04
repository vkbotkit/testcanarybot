import testcanarybot

bot = testcanarybot.Longpoll(
    "816be56e3b314cd7af06e361b948b0f6958e87c348e1c906726c15046214f36e91bf3aad22547635c10da", 
    195675828, testcanarybot.getPath(__file__)
    ) # 0 is a group_id

bot.setMentions('кб', 'канари', 'канарибот', 'каня', 'киоко', 'кань')
bot.setNameCases('каня', 'кани', 'кане', 'каню', 'каней')

bot.setObject(
    "ASSETS_ERROR", 
    "Чтобы получить описание модуля, отправьте {mention} библиотека описание {название модуля}"
    )

bot.setObject(
    "LIBRARY_PIC", 
    "photo-195675828_457241499"
    )
bot.setObject(
    "LIBRARY_RESPONSE_LIST", 
    "Библиотека, с которой работает {mention}:\n\n{plugins}\n\n Чтобы получить описание модуля, отправьте {mention} ассеты описание [название модуля]"
    )
bot.setObject(
    "LIBRARY_RESPONSE_LIST_ITEM", 
    "\u2022"
    )
bot.setObject(
    "LIBRARY_RESPONSE_ERROR", 
    "Такого модуля не существует :)"
    )
bot.setObject(
    "ERRORHANDLED_MESSAGE", 
    ["{user}, можешь повторить?", ]
    )
bot.setObject(
    "ERRORHANDLED_ATTACHMENT", 
    ["photo-195675828_457241495", ]
    )

bot.listen(None)