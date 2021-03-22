![https://pypi.org/project/testcanarybot/1.00.003/](https://img.shields.io/badge/pypi-1.0.003-blue?style=flat-square)![](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue?style=flat-square)![](https://img.shields.io/badge/license-Apache%20License%202.0-green?style=flat-square)

Асинхронная библиотека с прекрасной структурой модульной библиотекой обработчиков для ВКонтакте API, написанная на Python 3.7 с aiohttp, asyncio и threading

```bash
$ python -m testcanarybot --create SampleName --token 7a6fa4dff77a228eeda56603b8f53806c883f011c40b72630bb50df056f6479e52a --group 195675828
$ python -m testcanarybot --project SampleName --cm HandlerExample -f
$ python -m testcanarybot --run SampleName
```

* [Примеры](https://github.com/kensoi/testcanarybot/tree/dev/library)
* [Документация](https://kensoi.github.io/testcanarybot)
* [Сообщество ВКонтакте](https://vk.com/testcanarybot)
* [Блог Автора](https://vk.com/crubbukket)

## Установка

```bash
$ pip install testcanarybot 
```

## Создание бота

```bash
$ python -m testcanarybot --create BotName # после выполнения команды требуется настроить BotName/root.py
$ python -m testcanarybot --project BotName --create HandlerName 
```

## Способы запустить бота

```bash
$ python -m testcanarybot --run BotName
$ python -m testcanarybot -mrun --projects BotName1 BotName2 # для запуска нескольких проектов
$ python -m testcanarybot --run all # для запуска всех проектов в директории
```

|              | TESTCANARYBOT PRE-RELEASE PREVIEW      |
| :----------- | :------------------------------------- |
| Версия       | 01.00.003                              |
| Канал        | unstable                               |
| Документация | https://kensoi.github.io/testcanarybot |