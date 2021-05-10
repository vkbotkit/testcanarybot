# Обработчики

Пример с обработчиками можно найти по этой ссылке: [examples-reactions.py](https://github.com/kensoi/testcanarybot/blob/dev/library/examples-reactions.py)

Для упрощения работы обработчики должны быть занесены в специальный объект, образованный от objects.libraryModule:

```python
import random
from testcanarybot import objects
from testcanarybot import exceptions

class Main(objects.libraryModule):
    async def start(self, tools: objects.tools):
        pass
```

```Main.start``` - функция для запуска задачи, используется вместо ```__init__``` для взаимодействия с инструментами фреймворка. Принимает tools

другие корутины, обёрнутые с помощью декораторов, должны принимать tools и package.

## Обозначения

Приоритет (priority) - обработчик для команд бота

Войд (void) - обработчик для исключения ```exceptions.CallVoid(objects.task(package))```, незарегистрированных команд и иных сообщений, которые не содержат в себе команды.

## Контекстный менеджер (и альтернативы)

Это базовый декоратор для objects.libraryModule, который позволяет регистрировать обработчики для дальнейшей рассылки событий

```python
@objects.ContextManager(commands:list, events:list, action:list, private:bool)
async def HandlerName(self, tools: objects.tools, package: objects: package):
```

* **commands**: списки команд, например для ['привет', ['я', 'люблю', 'пончики']]. Обработчик будет получать сообщения "@вашбот привет всем" или "@вашбот я люблю пончики", т.е. по указанному ключу.
  
  * **Альтернатива**: декоратор ```objects.priority(commands: list)```
* **events**: для событий, см testcanarybot.enums.events
  
* **Альтернатива**: декоратор ```objects.event(events: list)```
  
* **action**: для конкретного события внутри беседы, см testcanarybot.enums.action

  * **Альтернатива**: декоратор ```objects.action(action: enums.action)```

* если ни один из данных аргументов не был определён, то весь обработчик будет зарегистрирован как **Void**, который получает оповещения в следующих случаях:

  * если вы настроили ALL_MESSAGES = True в root.py проекта, т.е. бот отправляет на обработку все сообщения. При значении False обрабатываются сообщения, в которых нулевое ключевое слово является упоминанием бота, а первое не зарегистрировано в проекте. Например:
    * "@apiclub hawo", если "hawo" не был найден в словаре команд
  * если в обработчиках для команд была вызвана ошибка exceptions.CallVoid(objects.task(package)), которая перенаправляет peer_id и from_id из события в Void обработчик
  * **Альтернатива**: декоратор ```objects.void```

  **[Примечание]** Контекстный менеджер является универсальной обёрткой для обработчиков, в случае если нужно обработать сообщения, например, которые содержат или команду или action.

  Декораторы ```objects.priority(commands: list)```, ```objects.event(events: list)```, ```objects.action(action: enums.action)``` используют Контекстный менеджер для своих частных случаев

# Tools

В этой главе расписаны методы из tools, которые принимает обработчик вместе с обрабатываемым событием

**Файловый менеджер для директории assets**

```python
tools.assets # works like open()

"""
with tools.assets("test.txt", 'r') as file: # ./assets/test.txt
	print(file.read())
"""
```


**Глобальные переменные**

```python
tools.values

# tools.values.get(name: str) -> expression if exists/empty expression (":::{name}:UNKNOWN:::")
# tools.values.set(name: str, value: typing.Optional[str] = None, type: enums.values)
# tools.values.switch(name: str, value: typing.Optional[bool] = None)
    # tools.values.type(name) should be values.tumbler
    # if not value: value = not tools.values.get(name)
# tools.values.getKeys [list]
```


**ВКонтакте API**

```python
tools.api		

# await tools.api.method
# tools.api.http
# await tools.api.messages.send(random_id, peer_id, message), e.t.c (vk.com/dev/methods)
```


**Сессия фреймворка**

```python
tools.http # [aiohttp.session]
```
P.S. следует использовать, т.к. рассчитано на многопоточность



**Получить рандомное значение от 0 до 999999**

```python
tools.gen_random()
```


**Сделать запись в лог**

```python
tools.system_message(*args, write: typing.Optional[str] = None, module: str = "system", level:str = 'info') # -> None	
```
args - строки через запятую (tools.system_message("a", "b", "c") -> "a b c") 

```write``` - целой строкой

```module``` - подпись сообщения

```level``` - уровень сообщения ```CRITICAL/ERROR/WARNING/INFO/DEBUG/NOTSET]```



**Получить ID бота**

```python
response = tools.getBotId(): # -> int		
```


**Получить упоминание бота в формате** ```apiclub``` **для бота из vk.com/club1** 

```python
response = tools.getBotLink(): # -> str	
```


**Получить упоминание бота через** ```objects.mention```

```python
response = tools.getBotDogMention() # -> objects.mention
response = repr(tools.getBotDogMention()) # -> [club1|@apiclub] for bot from vk.com/club1
```



**Получить список строк, установленных как упоминания бота через app.setMentions**

```python
response = tools.getBotMentions()  # -> list of str
```



**Проверить наличие пакетов, ожидающих ответа**

```python
response = tools.wait_check(package) # -> bool
```



**Получить ответ пользователя (только для package с type = events.message_new):**

```python
response = await tools.wait_reply(package) # -> objects.package [from reply]
```



**Получить упоминание в виде строки:**

```python 
response = await tools.getMention(page_id = None, name_case = "nom") # -> str
```

```name_case = "link"``` -> возвращает форму в виде ```[id1|@durov]``` (для 'nom', 'gen', 'dat', 'acc', 'ins', 'abl' возвращает имя в заданном падеже)

```page_id = None``` -> используется ID бота 



**Получить список участников группы с ID = group_id (если group_id = None, то используется ID чатбота):**

```python
response = await tools.getManagers(group_id = None) # -> list
```



**Проверить, является ли страница администратором паблика (если group_id = None, то используется ID чатбота):**

```python
response = await tools.isManager(from_id, group_id = None) # -> bool
```



**Список администраторов беседы:**

 ```python
response = await tools.getChatManagers(peer_id) # -> list of int
 ```



**Проверить, является ли страница администратором беседы:**

```python
response = await tools.isChatManager(from_id, peer_id) # -> bool
```



**Получить список участников данной беседы (список ID):**

```python
response = await tools.getMembers(peer_id) # -> list of int
```



**Проверить, является ли страница под данным ID участником данной беседы (возвращает bool):**

  ```python
response = await tools.isMember(from_id, peer_id) # -> bool
  ```

  