import logging
import os
from time import sleep

import requests
from dotenv import load_dotenv

from tg_notifictaion_bot import TgNotificationBot, TelegramLogsHandler

logger = logging.getLogger(__file__)


def get_response_from_dvmn(headers, params):
    url = 'https://dvmn.org/api/long_polling/'

    response = requests.get(url, headers=headers, params=params, timeout=91)
    response.raise_for_status()
    return response.json()


def main():
    load_dotenv()

    dvmn_token = os.getenv('DVMN_TOKEN')
    bot_token = os.getenv('BOT_TOKEN')
    chat_id = os.getenv('CHAT_ID')

    bot = TgNotificationBot(bot_token, dvmn_token, chat_id)

    tg_handler = TelegramLogsHandler(bot.bot, chat_id)
    logger.addHandler(tg_handler)
    logger.warning('Бот запущен')

    params = {}
    headers = {
        'Authorization': f'Token {dvmn_token}',
    }
    while True:
        try:
            dvmn_response = get_response_from_dvmn(headers, params)
        except requests.exceptions.ReadTimeout:
            logger.info('The response from the server was not received')
        except requests.exceptions.ConnectionError:
            logger.info('Problems with Internet connection')
            sleep(300)
        except Exception as err:
            logger.exception(err)
            break
        else:
            response_status = dvmn_response['status']
            if response_status == 'found':
                timestamp = dvmn_response['last_attempt_timestamp']
                bot.send_message_to_user(dvmn_response['new_attempts'])
            else:
                timestamp = dvmn_response['timestamp_to_request']
            params.update({'timestamp': timestamp})


if __name__ == '__main__':
    main()
