# Install and try testcanarybot

Чтобы использовать testcanarybot для создания бота, вам нужно установить фреймворк на ваш компьютер. Перед этим требуется установить Python 3.7 и удобную среду для разработки.

Также требуется создать сообщество, через которое чатбот будет отвечать на сообщения. 

По ссылке vk.com/{yourcommunity}?act=tokens создайте ключ доступа. 

По ссылке vk.com/{yourcommunity}?act=longpoll_api настройте ваш Longpoll сервер, через который ваш бот будет получать и обрабатывать уведомления.

## Install

#### Install with PIP

Установив Python, откройте командную строку от имени администратора и введите следующую команду:

`pip install testcanarybot`

Если вы уже используете testcanarybot, то можно обновить его такой командой

`pip install --upgrade testcanarybot`

#### Install with Github

Если вы используете github, то установить или обновить testcanarybot можно следующими командами в зависимости от нужного канала обновлений:

**Stable** -- релизы проверенных версий testcanarybot

`pip install [--upgrade] https://github.com/kensoi/testcanarybot/tarball/stable`

**Unstable** -- законченные версии testcanarybot в тестировании

`pip install [--upgrade] https://github.com/kensoi/testcanarybot/tarball/unstable`

**Dev** -- сырые версии testcanarybot с малым количеством изменений

`pip install [--upgrade] https://github.com/kensoi/testcanarybot/tarball/dev`

## Manual "How to create your first bot"

После установки можно заняться изучением фреймворка.

Для вашего проекта требуется выделить отдельный каталог, в котором будет содержаться библиотека, которую использует testcanarybot для работы вашего чатбота. Создайте файл (к примеру app.py) с любым названием в каталоге и впишите в него следующий код:

```python
import testcanarybot

bot = testcanarybot.app(
    access_token = {your_token},
    groupId = {your community id},
    countThread = 1
    )

bot.start_polling()
```

Open terminal at your project directory and run this command:

```bash
$ python -m testcanarybot -cf #creating directories for assets and library
Creating directories...
Creating readme files...
Done! Look new files at created folders: ./assets/ and ./library/
```

And this. How you can see, bot didn't started and raised the Library Error, let's see what happened:

```bash
$ python app.py
@bot.session: started
@bot.library.uploader: library directory is listed
Traceback (most recent call last):
  File "app.py", line 19, in <module>
    bot.start_polling()
  File "C:\Program Files\Python\lib\site-packages\testcanarybot\framework\_application.py", line 228, in start_polling
    self.setup()
  File "C:\Program Files\Python\lib\site-packages\testcanarybot\framework\_application.py", line 204, in setup        
    self.__library.upload()
  File "C:\Program Files\Python\lib\site-packages\testcanarybot\framework\_library.py", line 36, in upload
    self.tools.values.LIBRARY_ERROR)
testcanarybot.exceptions.LibraryError: library directory is broken
@bot.session: closed
```

Твоя библиотека повреждена, это говорит о неналичии никаких модулей внутри её директории. Для решения можно скачать примеры модулей с Github репозитория или воспользоваться этой командой:

```bash
$ python -m testcanarybot -cm --name testHandler
parsing module name...
writing code example...
Done! Result ./library/testhandler.py
```

Results at ./library/testHandler.py:

```python
from testcanarybot import objects
from testcanarybot import exceptions #handling and raising errors
"""
(c) kensoi.github.io, since 2020
"""
class Main(objects.libraryModule):
	async def start(self, tools: objects.tools):
		pass # create task at start

	@objects.ContextManager(commands = ["check"])
	async def ContextManagerHandler(self, tools: objects.tools, package: objects.package):
		await tools.api.message.send(random_id = tools.random_id, peer_id = package.peer_id, message = "handler is working!")
```

Trying to run app.py again:

```bash
$python test.py
@bot.session: started
@bot.library.uploader: library directory is listed  
@bot.library.uploader: library.testhandler is loaded
                 + registered 1 commands

@bot.library.uploader: Supporting event types:      
                events.message_new

@bot.package_handler: handler_0 is started
@bot.longpoll: server updated

@bot.longpoll: polling is started 
```

Success! Now try to send a message "@{your bot address} check" to your community.