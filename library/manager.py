v = 0.6
name = """Управление подписками"""
descr = """{group_mention} subman mngrs [admins/none/список упоминаний] - установить список
{group_mention} subman mngrs_add [список упоминаний] - добавить людей в список
{group_mention} subman mngrs_del [список упоминаний] - убрать определённных людей из списка
{group_mention} subman show - показать список
{group_mention} subman remove_myself"""


response_success_add = "Люди успешно внесены в список. Чтобы подписка отправляла сообщения, разрешите боту "
response_success_del = "Люди успешно удалены из списка."
response_error_checklist = "В списке нет упоминаний пользователей для установки лайкнувших"
response_success_list = "Список людей, которых добавили в список отслежки активности в группе: {listd}"


def init(tools):
    global plugintype, descr
    plugintype = [
        tools.events.MESSAGE_NEW
    ]
    descr = descr.format(group_mention = tools.group_mention)

    tools.setObject("ADMIN_SUB", tools.getManagers(tools.group_id))


def update(tools, package):
    if package["text"][0] == "subman" and package["from_id"] in (tools.getManagers(tools.group_id) or tools.getObject("ADMIN_SUB")):
        peep = package["from_id"] in tools.getManagers(tools.group_id)
        
        if peep:
            if package["text"][1] == "mngrs":
                if package["text"][2] == "admins":
                    managers = tools.getManagers(tools.group_id)

                elif package["text"][2] == "none":
                    managers = []

                else:
                    managers = package["text"][2:-1]

                    if not tools.checklist(managers, int):
                        managers = []
                        
                        tools.api.messages.send(
                            random_id = tools.random_id(), 
                            message = response_error_checklist, 
                            peer_id = package["peer_id"])
                        return 1

                tools.setObject("ADMIN_SUB", managers)
                tools.api.messages.send(
                    random_id = tools.random_id(), 
                    message = response_success_add, 
                    peer_id = package["peer_id"]
                    )
                return 1

            elif package["text"][1] == "mngrs_add":
                managers = package["text"][2:-1]

                if not tools.checklist(managers, int):
                    managers = []

                    tools.api.messages.send(
                        random_id = tools.random_id(), 
                        message = response_error_checklist, 
                        peer_id = package["peer_id"]
                        )
                    return 1
                    
                for i in managers:
                    if i not in tools.getObject("ADMIN_SUB"): tools.getObject("ADMIN_SUB").append(managers)
                
                tools.api.messages.send(
                    random_id = tools.random_id(), 
                    message = response_success_add, 
                    peer_id = package["peer_id"]
                    )
                return 1

            elif package["text"][1] == "mngrs_del":
                managers = package["text"][2:-1]

                if not tools.ischecktype(managers, int):
                    managers = []

                    tools.api.messages.send(
                        random_id = tools.random_id(), 
                        message = response_error_checklist, 
                        peer_id = package["peer_id"]
                        )
                    return 1
                    
                for i in managers:
                    if i in tools.getObject("ADMIN_SUB"): tools.getObject("ADMIN_SUB").remove(i)

                tools.api.messages.send(
                    random_id = tools.random_id(), 
                    message = response_success_del, 
                    peer_id = package["peer_id"]
                    )
                return 1

            elif package["text"][1] == "show":
                tools.api.messages.send(
                    random_id = tools.random_id(), 
                    message = response_success_list.format(
                        listd = " ".join(
                            [tools.getMention(i, 'link') for i in tools.getObject("ADMIN_SUB")]
                            )
                        ), 
                    peer_id = package["peer_id"]
                )
                return 1

        elif package["text"][1] == "remove_myself":
            if package['from_id'] in tools.getObject("ADMIN_SUB"):
                tools.getObject("ADMIN_SUB").remove(package['from_id'])
            
            tools.api.messages.send(
                random_id = tools.random_id(), 
                message = response_success_list, 
                peer_id = package["peer_id"]
                )
            return 1
            
        elif package["test"][1] == "help":
            return [
                tools.getObject("LIBRARY_SYNTAX"),
                "manager.py"
            ]