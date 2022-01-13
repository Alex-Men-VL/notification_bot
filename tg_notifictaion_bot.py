import logging

import telegram

import static_text
from keyboard_utils import make_keyboard_with_lesson_url


class TelegramLogsHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.bot = bot

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


class LoggingMixin:
    def __getattr__(self, name):
        if name in ['critical', 'error', 'warning', 'info', 'debug']:
            if not hasattr(self.__class__, '__logger'):
                self.__class__.__logger = logging.getLogger(
                    self.__class__.__module__
                )
                self.__class__.__logger.setLevel(logging.WARNING)
                self.__class__.__logger.addHandler(
                    TelegramLogsHandler(self.bot, self.chat_id)
                )
            return getattr(self.__class__.__logger, name)


class TgNotificationBot(LoggingMixin):
    def __init__(self, bot_token, dvmn_token, chat_id):
        self.bot = telegram.Bot(token=bot_token)
        self.dvmn_token = dvmn_token
        self.chat_id = chat_id

        self.warning('Бот запущен')

    def send_message_to_user(self, attempts_description):
        for attempt_description in attempts_description:
            if attempt_description['is_negative']:
                message_text = static_text.negative_message.format(
                    lesson_title=attempt_description['lesson_title']
                )
                reply_markup = make_keyboard_with_lesson_url(
                    attempt_description['lesson_url']
                )
            else:
                message_text = static_text.positive_message(
                    lesson_title=attempt_description['lesson_title']
                )
                reply_markup = None

            self.bot.send_message(chat_id=self.chat_id,
                                  text=message_text,
                                  reply_markup=reply_markup)
