# Установка testcanarybot 1.3.0
Вы можете установить testcanarybot двумя способами: через pypi и через github

#### 1. PYPI

```bash
$ pip3 install [--upgrade] testcanarybot
```

#### 2. Github

На github testcanarybot выпускается по трём каналам в соответствующие ветки:

**Stable** -- полностью протестированные версии

```bash
$ pip3  install [--upgrade] https://github.com/kensoi/testcanarybot/tarball/stable`
```

**Unstable** -- сырые версии, требующие тестирования

```bash
$ pip3  install [--upgrade] https://github.com/kensoi/testcanarybot/tarball/unstable`
```

**Dev** -- ветка для разработки (самые свежие нововведения)

```bash
$ pip3  install [--upgrade] https://github.com/kensoi/testcanarybot/tarball/dev`
```

Примечание: для работы с фреймворком смотрите [мануал для TPPM](./tppm.md)