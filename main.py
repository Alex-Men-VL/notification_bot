import logging
import os

import requests
import telegram
from dotenv import load_dotenv

import static_text
from keyboard_utils import make_keyboard_with_lesson_url


def get_response_from_dvmn(headers, params):
    url = 'https://dvmn.org/api/long_polling/'

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def send_message_to_user(bot, chat_id, attempts_description):
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

        bot.send_message(chat_id=chat_id,
                         text=message_text,
                         reply_markup=reply_markup)


def main():
    logging.basicConfig(level=logging.INFO)
    load_dotenv()

    dvmn_token = os.getenv('DVMN_TOKEN')
    bot_token = os.getenv('BOT_TOKEN')
    chat_id = os.getenv('CHAT_ID')

    bot = telegram.Bot(token=bot_token)
    params = {}
    headers = {
        'Authorization': f'Token {dvmn_token}',
    }
    while True:
        try:
            decoded_response = get_response_from_dvmn(headers, params)
        except requests.exceptions.ReadTimeout:
            logging.info('The response from the server was not received')
        except requests.exceptions.ConnectionError:
            logging.info('Problems with Internet connection')
        else:
            response_status = decoded_response['status']
            if response_status == 'found':
                send_message_to_user(bot, chat_id,
                                     decoded_response['new_attempts'])
            elif response_status == 'timeout':
                timestamp = decoded_response['timestamp_to_request']
                params.update({'timestamp': timestamp})


if __name__ == '__main__':
    main()
