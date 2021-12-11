from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import static_text


def make_keyboard_with_lesson_url(url) -> InlineKeyboardMarkup:
    button = [
        [InlineKeyboardButton(static_text.button_text, url=url)]
    ]

    reply_markup = InlineKeyboardMarkup(button)
    return reply_markup
