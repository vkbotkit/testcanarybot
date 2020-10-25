from vk_api.bot_longpoll import VkBotEventType


MENTION = ":::CANARYBOT:MENTION:::"
ENDLINE = ":::CANARYBOT:ENDMESSAGE:::"
ACTION = ":::CANARYBOT:ACTION:::"
PAYLOAD = ":::CANARYBOT:PAYLOAD:::"
NOREACT = ":::CANARYBOT:NOREACT:::"


MESSAGE_NEW = VkBotEventType.MESSAGE_NEW
LIKE_ADD = ":::CANARYBOT:LIKEADD:::"
LIKE_REMOVE = ":::CANARYBOT:LIKEADDREMOVE:::"


PLUGIN_LOAD = "plugin list is loaded, to update use \"self.all = self.getPlugins()\""
PLUGIN_INIT = "initialisation"

PLUGIN_FAILED_BROKEN = "Broken ({})"
PLUGIN_FAILED_NOSUPP = "Plugin version is not supported"
PLUGIN_FAILED_NOUPD = "No 'update' function"


ERROR_HANDLER = ":::CANARYBOT:ERROR_HANDLER:::"

LIBRARY_SYNTAX = ":::CANARYBOT:LIBRARY_SYNTAX:::"
PARSER_SYNTAX = ":::CANARYBOT:PARSER:::"

ASSETS_ERROR = ""

LIBRARY_ERROR = ":::CANARYBOT:LIBRARY_ERROR:::"
LIBRARY_NOSELECT = ":::CANARYBOT:LIBRARY_NOSELECT:::"
LIBRARY_PIC = ""

LIBRARY_RESPONSE_LIST = ""
LIBRARY_RESPONSE_LIST_ITEM = ""
LIBRARY_RESPONSE_ERROR = ""
LIBRARY_RESPONSE_DESCR = "{name}: {descr}"


class responses:
    def __init__(self):
        pass