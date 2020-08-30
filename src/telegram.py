import telegram
import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

def send(msg, chat_id = CHAT_ID, bot_token = BOT_TOKEN):
    """
    Send a mensage to a telegram user specified on chatId
    chat_id must be a number!
    """
    bot = telegram.Bot(token=bot_token)
    bot.sendMessage(chat_id=chat_id, text=msg)


class emoji:
    '''reference:
     https://apps.timwhitlock.info/emoji/tables/unicode'''

    double_exclamation = b'\xE2\x80\xBC'.decode("utf-8")
    play = b'\xE2\x96\xB6'.decode("utf-8")
    check = b'\xE2\x9C\x85'.decode("utf-8")
    hourglass = b'\xE2\x8F\xB3'.decode("utf-8")
    cross = b'\xE2\x9D\x8C'.decode("utf-8")
