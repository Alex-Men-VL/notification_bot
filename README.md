# Уведомления о проверенных работах

## Описание проекта

Скрипт отправляет сообщение в телеграм, если появилась новая проверенная работа
на сайте [dvmn.org](https://dvmn.org/)

Все логи бота также отправляются в сообщении в телеграм.

## Как запустить

Скачайте код:

```bash
$ git clone https://github.com/Alex-Men-VL/notification_bot.git
$ cd notification_bot
```

Установите зависимости:

```bash
$ pip install -r requirements.txt
```

Запустите скрипт командой:

```bash
$ python3 main.py
```

### Локальный запуск через Docker

Создайте образ командой:

```shell
docker build -t tg_bot .
```

Запустите контейнер командой:

```shell
docker run -d --env-file .env tg_bot
```

Проверьте статус созданного контейнера:

```shell
docker ps -a
```

При наличии ошибок, проверьте логи:

```shell
docker logs <ID контейнера>
```

## Деплой на Heroku с помощью Dockerfile

Создайте приложение на Heroku:

```shell
$ heroku login
$ heroku create
$ heroku git:remote -a <название приложения>
```

Добавьте переменные окружения:

```shell
$ heroku config:set <ПЕРЕМЕННАЯ=значение>
```

Установите `stack` вашего приложения в режим `container`:

```shell
$ heroku stack:set container
```

Отправьте свое приложение на Heroku

```shell
$ git push heroku main
```

## Переменные окружения

Часть данных берется из переменных окружения. Чтобы их определить, создайте файл `.env` 
рядом с `main.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`

Доступны три переменные:
- `DVMN_TOKEN` - токен с сайта [dvmn.org](https://dvmn.org/api/docs/);
- `BOT_TOKEN` - токен телеграм бота;
  - Чтобы его получить, напишите в Telegram специальному боту: `@BotFather`
- `CHAT_ID` - id вашего чата в телеграм.
  - Чтобы получить свой `chat_id`, напишите в Telegram специальному боту: `@userinfobot`

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/)