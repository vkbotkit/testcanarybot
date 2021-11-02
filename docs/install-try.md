# Install and try testcanarybot 0.9.1-dev10
## Requirements

- Python 3.7
- VK Community
- Access token (group auth)
- **[OPTIONAL] Service token**

## Install

You can install testcanarybot with PYPI or GitHub:

#### Install with PIP

```bash
pip install [--upgrade] testcanarybot
```

#### Install with GitHub

**Stable** -- tested versions of testcanarybot

```bash
pip install [--upgrade] https://github.com/kensoi/testcanarybot/tarball/stable`
```

**Unstable** -- raw versions of testcanarybot

```bash
pip install [--upgrade] https://github.com/kensoi/testcanarybot/tarball/unstable`
```

**Dev** -- development branch

```bash
pip install [--upgrade] https://github.com/kensoi/testcanarybot/tarball/dev`
```

## Manual "How to create your first bot"

Create an root file (for example app.py) and paste this code:

```python
import testcanarybot

bot = testcanarybot.app(
    access_token = {your access token},
    #service_token = {your service token| optional},
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

$ 
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

$
```

"Library directory is broken", it says that library is empty or all modules are corrupted.

Try to create sample module:

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

Executing root file with created module:

```bash
$ python app.py
@bot.session: started
@bot.library.uploader: library directory is listed  
@bot.library.uploader: library.testhandler is loaded # see, this is your module!
                 + registered 1 commands

@bot.library.uploader: Supporting event types:      
                events.message_new

@bot.package_handler: handler_0 is started
@bot.longpoll: server updated

@bot.longpoll: polling is started 
```

Success! Now open your.