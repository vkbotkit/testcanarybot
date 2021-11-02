<p align="center">
    <a href = "http://kensoi.github.io/testcanarybot/">
        <img src="/docs/pc-cover.png" alt="kensoi/testcanarybot" />
    </a>
</p>
# testcanarybot
async framework for vk chatbots


### simple bot run script example
There's a sample of your simple bot
```
import testcanarybot

token = """7a6fa4dff77a228eeda56603b8f53806c883f011c40b72630bb50df056f6479e52a"""
group_id = 1 # your community id

bot = testcanarybot.app(token = token, group_id = group_id)
bot.install()
bot.listen()
```
## Guides
First bot manual -- http://kensoi.github.io/testcanarybot/firstbot.html  
Creating testcanarybot module manual -- http://kensoi.github.io/testcanarybot/createmodule.html  

## Testcanarybot instruments
Events -- http://kensoi.github.io/testcanarybot/events.html  
Objects -- http://kensoi.github.io/testcanarybot/objects.html  

### Tools
Handler tools -- http://kensoi.github.io/testcanarybot/tools/handlers.html  
Assets -- http://kensoi.github.io/testcanarybot/tools/assets.html  
Keyboard -- http://kensoi.github.io/testcanarybot/tools/keyboard.html  
Uploader -- http://kensoi.github.io/testcanarybot/tools/upload.html  

## Examples
[root examples](https://github.com/kensoi/testcanarybot/tree/master/examples/bot)  
[module examples](https://github.com/kensoi/testcanarybot/tree/master/examples/modules)  
