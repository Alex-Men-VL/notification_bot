import telegram

import static_text
from keyboard_utils import make_keyboard_with_lesson_url


class TgNotificationBot(object):

    def __init__(self, bot_token, dvmn_token, chat_id):
        self.bot = telegram.Bot(token=bot_token)
        self.dvmn_token = dvmn_token
        self.chat_id = chat_id

    def send_message_to_user(self, chat_id, attempts_description):
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

            self.bot.send_message(chat_id=chat_id,
                                  text=message_text,
                                  reply_markup=reply_markup)
