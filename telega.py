import config
from telegram.ext import Updater


def send_msg(message):
    for i in range(3):
        try:
            updater = Updater(config.TOKEN,
                              # request_kwargs=REQUEST_KWARGS,
                              use_context=True)
            for user_id, msg_list in message.items():
                message = '\n'.join(msg_list)

                if user_id == 1:
                    updater.bot.send_message(chat_id=config.BOT_FATHER,
                                             text=message,
                                             parse_mode='HTML',
                                             disable_web_page_preview=True)
                if user_id == 18:
                    updater.bot.send_message(chat_id=config.ALEX,
                                             text=message,
                                             parse_mode='HTML',
                                             disable_web_page_preview=True)
                if user_id == 2:
                    updater.bot.send_message(chat_id=config.DOZ,
                                             text=message,
                                             parse_mode='HTML',
                                             disable_web_page_preview=True)
                if user_id == 13:
                    updater.bot.send_message(chat_id=config.OLEG,
                                             text=message,
                                             parse_mode='HTML',
                                             disable_web_page_preview=True)
        except Exception as e:
            print(e)
        else:
            break
