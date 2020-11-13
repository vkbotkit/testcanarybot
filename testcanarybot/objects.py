from vk_api.bot_longpoll import VkBotEventType
from enum import Enum

class responses:
    def __init__(self):
        pass

class events_cover:
    def __init__(self):
        self.list_of_types = []

class expressions_cover:
    def __init__(self):
        self.list_of_exp = []


resource = {
    'from_id': [
        'deleter_id', 
        'liker_id',
        'user_id'
        ],
    'peer_id': [
        'market_owner_id', 'owner_id', 'object_owner_id', 
        'post_owner_id', 'photo_owner_id', 'topic_owner_id', 
        'video_owner_id', 'to_id'
        ]
}


package_sample = {
        'id': 0,
        'date': 0,
        'random_id': 0,
        'peer_id': 1,
        'from_id': 1,
        'attachments': [],
        'payload': '',
        'keyboard': {},
        'fwd_messages': [],
        'reply_message': {},
        'action': {},
        'conversation_message_id': '',
        'plugin_type': '',
        'text': [],
    }


def object_handler(tools, event, obj):
    package = package_sample
    package['peer_id'] = tools.group_id

    for key, value in obj.items():
        for i, j in resource.items():
            if key in j: package[i] = value

        package[key] = value
    
    package['text'].append(event)
    package['text'].append(tools.getObject("ENDLINE"))
    package['plugintype'] = getattr(tools.objects.events, event)

    return package


events = events_cover()
exp = expressions_cover()


def setEventType(name, value):
    global events
    setattr(events, name, str(value))
    events.list_of_types.append(name)


def setExpression(name, value = None):
    if not value:
        value = name

    global exp
    setattr(exp, name, value)
    exp.list_of_exp.append(name)


setExpression("MENTION", ":::CANARYBOT:MENTION:::")
setExpression("ENDLINE", ":::CANARYBOT:ENDMESSAGE:::")
setExpression("ACTION", ":::CANARYBOT:ACTION:::")
setExpression("PAYLOAD", ":::CANARYBOT:PAYLOAD:::")
setExpression("NOREACT", ":::CANARYBOT:NOREACT:::")
setExpression("START_LOGGER", "START_LOGGER")
setExpression("FWD_MES", "forwarded messages")


setEventType("MESSAGE_NEW", VkBotEventType.MESSAGE_NEW)
setEventType("MESSAGE_ALLOW", VkBotEventType.MESSAGE_ALLOW)
setEventType("MESSAGE_DENY", VkBotEventType.MESSAGE_DENY)
setEventType("MESSAGE_EVENT", VkBotEventType.MESSAGE_EVENT)

setEventType("PHOTO_NEW", VkBotEventType.PHOTO_NEW)
setEventType("PHOTO_COMMENT_NEW", VkBotEventType.PHOTO_COMMENT_NEW)
setEventType("PHOTO_COMMENT_EDIT", VkBotEventType.PHOTO_COMMENT_EDIT)
setEventType("PHOTO_COMMENT_RESTORE", VkBotEventType.PHOTO_COMMENT_RESTORE)
setEventType("PHOTO_COMMENT_DELETE", VkBotEventType.PHOTO_COMMENT_DELETE)

setEventType("AUDIO_NEW", VkBotEventType.AUDIO_NEW)

setEventType("VIDEO_NEW", VkBotEventType.VIDEO_NEW)
setEventType("VIDEO_COMMENT_NEW", VkBotEventType.VIDEO_COMMENT_NEW)
setEventType("VIDEO_COMMENT_EDIT", VkBotEventType.VIDEO_COMMENT_EDIT)
setEventType("VIDEO_COMMENT_RESTORE", VkBotEventType.VIDEO_COMMENT_RESTORE)
setEventType("VIDEO_COMMENT_DELETE", VkBotEventType.VIDEO_COMMENT_DELETE)

setEventType("WALL_POST_NEW", VkBotEventType.WALL_POST_NEW)
setEventType("WALL_REPOST", VkBotEventType.WALL_REPOST)
setEventType("WALL_REPLY_NEW", VkBotEventType.WALL_REPLY_NEW)
setEventType("WALL_REPLY_EDIT", VkBotEventType.WALL_REPLY_EDIT)
setEventType("WALL_REPLY_RESTORE", VkBotEventType.WALL_REPLY_RESTORE)
setEventType("WALL_REPLY_DELETE", VkBotEventType.WALL_REPLY_DELETE)

setEventType("BOARD_POST_NEW", VkBotEventType.BOARD_POST_NEW)
setEventType("BOARD_POST_EDIT", VkBotEventType.BOARD_POST_EDIT)
setEventType("BOARD_POST_RESTORE", VkBotEventType.BOARD_POST_RESTORE)
setEventType("BOARD_POST_DELETE", VkBotEventType.BOARD_POST_DELETE)

setEventType("MARKET_COMMENT_NEW", VkBotEventType.MARKET_COMMENT_NEW)
setEventType("MARKET_COMMENT_EDIT", VkBotEventType.MARKET_COMMENT_EDIT)
setEventType("MARKET_COMMENT_RESTORE", VkBotEventType.MARKET_COMMENT_RESTORE)
setEventType("MARKET_COMMENT_DELETE", VkBotEventType.MARKET_COMMENT_DELETE)
setEventType("MARKET_ORDER_NEW", ":::CANARYBOT:MARKET_ORDER_NEW:::")
setEventType("MARKET_ORDER_EDIT", ":::CANARYBOT:MARKET_ORDER_EDIT:::")

setEventType("GROUP_LEAVE", VkBotEventType.GROUP_LEAVE)
setEventType("GROUP_JOIN", VkBotEventType.GROUP_JOIN)

setEventType("USER_BLOCK", VkBotEventType.USER_BLOCK)
setEventType("USER_UNBLOCK", VkBotEventType.USER_UNBLOCK)

setEventType("POLL_VOTE_NEW", VkBotEventType.POLL_VOTE_NEW)

setEventType("GROUP_OFFICERS_EDIT", VkBotEventType.GROUP_OFFICERS_EDIT)
setEventType("GROUP_CHANGE_SETTINGS", VkBotEventType.GROUP_CHANGE_SETTINGS)
setEventType("GROUP_CHANGE_PHOTO", VkBotEventType.GROUP_CHANGE_PHOTO)

setEventType("VKPAY_TRANSACTION", VkBotEventType.VKPAY_TRANSACTION)
setEventType("APP_PAYLOAD", ":::CANARYBOT:APP_PAYLOAD:::")

setEventType("LIKE_ADD", ":::CANARYBOT:LIKEADD:::")
setEventType("LIKE_REMOVE", ":::CANARYBOT:LIKEREMOVE:::")
setEventType("ERROR_HANDLER", ":::CANARYBOT:ERROR_HANDLER:::")

setExpression("PLUGIN_LOAD", "plugin list is loaded, to update use \"self.all = self.getPlugins()\"")
setExpression("PLUGIN_INIT", "initialisation")

setExpression("PLUGIN_FAILED_BROKEN", "Broken ({})")
setExpression("PLUGIN_FAILED_NOSUPP", "Plugin version is not supported")
setExpression("PLUGIN_FAILED_NOUPD", "No 'update' function")
setExpression("PLUGIN_FAILED_NONAME", "This plugin does not have a name.")
setExpression("PLUGIN_FAILED_NODESCR", "This plugin does not have a description.")
setExpression("CONSOLE_SYNTAX", "")

setExpression("BEEPA_PAPASA", ":::NYASHKA:NYASHKA:::")

setExpression("LIBRARY_SYNTAX", ":::CANARYBOT:LIBRARY_SYNTAX:::")
setExpression("PARSER_SYNTAX", ":::CANARYBOT:PARSER:::")

setExpression("ASSETS_ERROR", "ASSETS_ERROR")

setExpression("LIBRARY_ERROR", ":::CANARYBOT:LIBRARY_ERROR:::")
setExpression("LIBRARY_NOSELECT", ":::CANARYBOT:LIBRARY_NOSELECT:::")
setExpression("LIBRARY_PIC", "LIBRARY_PIC")

setExpression("LIBRARY_RESPONSE_LIST", "LIBRARY_RESPONSE_LIST")
setExpression("LIBRARY_RESPONSE_LIST_ITEM", "\u2022")
setExpression("LIBRARY_RESPONSE_ERROR", "LIBRARY_RESPONSE_ERROR")
setExpression("LIBRARY_RESPONSE_DESCR", "{name}: \n{descr} ")