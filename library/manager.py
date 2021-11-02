class lib_plugin():
    def __init__(self, api, tools):
        self.v = "0.4.0"
        self.descr = 'test plugin'

        self.response_success_add = "Люди успешно внесены в список. Чтобы подписка отправляла сообщения, разрешите боту "
        self.response_success_del = "Люди успешно удалены из списка."
        self.response_error_checklist = "В списке нет упоминаний пользователей для установки лайкнувших"
        self.response_success_list = "Список людей, которых добавили в список отслежки активности в группе: {listd}"
        tools.setObject("ADMIN_SUB", tools.getManagers(tools.group_id))


    def update(self, api, tools, package):
        if package["text"][0] == "subman" and package["from_id"] in (tools.getManagers(tools.group_id) or tools.objects.ADMIN_SUB):
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
                            
                            api.messages.send(
                                random_id = tools.random_id(), 
                                message = self.response_error_checklist, 
                                peer_id = package["peer_id"])
                            return 1

                    tools.setObject("ADMIN_SUB", managers)
                    api.messages.send(
                        random_id = tools.random_id(), 
                        message = self.response_success_add, 
                        peer_id = package["peer_id"]
                        )
                    return 1

                elif package["text"][1] == "mngrs_add":
                    managers = package["text"][2:-1]

                    if not tools.checklist(managers, int):
                        managers = []

                        api.messages.send(
                            random_id = tools.random_id(), 
                            message = self.response_error_checklist, 
                            peer_id = package["peer_id"]
                            )
                        return 1
                        
                    for i in managers:
                        if i not in tools.objects.ADMIN_SUB: tools.objects.ADMIN_SUB.append(managers)
                    
                    api.messages.send(
                        random_id = tools.random_id(), 
                        message = self.response_success_add, 
                        peer_id = package["peer_id"]
                        )
                    return 1

                elif package["text"][1] == "mngrs_del":
                    managers = package["text"][2:-1]

                    if not tools.ischecktype(managers, int):
                        managers = []

                        api.messages.send(
                            random_id = tools.random_id(), 
                            message = self.response_error_checklist, 
                            peer_id = package["peer_id"]
                            )
                        return 1
                        
                    for i in managers:
                        if i in tools.objects.ADMIN_SUB: tools.objects.ADMIN_SUB.remove(i)

                    api.messages.send(
                        random_id = tools.random_id(), 
                        message = self.response_success_del, 
                        peer_id = package["peer_id"]
                        )
                    return 1

                elif package["text"][1] == "show":
                    api.messages.send(
                        random_id = tools.random_id(), 
                        message = self.response_success_list.format(
                            listd = " ".join(
                                [tools.getMention(i, 'link') for i in tools.objects.ADMIN_SUB]
                                )
                            ), 
                        peer_id = package["peer_id"]
                    )
                    return 1

            elif package["text"][1] == "remove_myself":
                if package['from_id'] in tools.objects.ADMIN_SUB:
                    tools.objects.ADMIN_SUB.remove(package['from_id'])
                
                api.messages.send(
                    random_id = tools.random_id(), 
                    message = self.response_success_list, 
                    peer_id = package["peer_id"]
                    )
                return 1