![https://pypi.org/project/testcanarybot/1.3.1/](https://img.shields.io/badge/pypi-1.3.1-blue?style=flat-square) ![](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue?style=flat-square) ![](https://img.shields.io/badge/license-Apache%20License%202.0-green?style=flat-square)

testcanarybot is simple asynchronous bot framework for VK Bot API written in Python 3.7 with asyncio, aiohttp and threading.

## Links

* [Examples](https://github.com/kensoi/testcanarybot/tree/stable/library)
* [Documentation](https://kensoi.github.io/testcanarybot)
* [VK Community](https://vk.com/testcanarybot)

## Bot application sample

```python
import testcanarybot
import config # token, group_id

bot = testcanarybot.app(config.token, config.group_id)
bot.start_polling()
```

* [Examples](https://github.com/kensoi/testcanarybot/tree/v1.x/library)
* [Documentation](https://kensoi.github.io/testcanarybot)
* [VK Community](https://vk.com/testcanarybot)
* [VK Author blog](https://vk.com/crubbukket)

## Install

```bash
$ pip3 install testcanarybot 
```