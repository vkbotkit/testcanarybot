import testcanarybot

bot = testcanarybot.Longpoll(
    "token", 
    0, testcanarybot.getPath(__file__)
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