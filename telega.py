import config
from telegram.ext import Updater


def send_msg(message):
    for i in range(3):
        try:
            REQUEST_KWARGS = {
                'proxy_url': 'socks5h://orbtl.s5.opennetwork.cc:999',
                'urllib3_proxy_kwargs': {
                    'username': config.BOT_FATHER,
                    'password': 'F2fL3J74',
                }
            }
            updater = Updater(config.TOKEN,
                              # request_kwargs=REQUEST_KWARGS,
                              use_context=True)
            updater.bot.send_message(chat_id=config.BOT_FATHER,
                                     text=message,
                                     parse_mode='HTML',
                                     disable_web_page_preview=True)
            updater.bot.send_message(chat_id=config.ALEX,
                                     text=message,
                                     parse_mode='HTML',
                                     disable_web_page_preview=True)
            updater.bot.send_message(chat_id=config.DOZ,
                                     text=message,
                                     parse_mode='HTML',
                                     disable_web_page_preview=True)
        except Exception as e:
            print(e)
        else:
            break
