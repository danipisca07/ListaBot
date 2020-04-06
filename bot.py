import telepot
import logging
import os


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

TOKEN = os.getenv("TOKEN")

lista = list()

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    txt = msg['text']
    logger.info("Ricevuto messaggio {} da id {}".format(txt, chat_id))
    if content_type == 'text':
        name = msg["from"]["first_name"]
        if '/start' in txt:
            bot.sendMessage(chat_id, 'Benvenuto {}, per aggiungere nuove voci alla lista della spesa invia un messaggio contenente il nome dell\' oggetto da aggiungere. Per visualizzare la lista digita /lista.'.format(name, chat_id))
        elif '/id' in txt:
            bot.sendMessage(chat_id, 'Il tuo ID e\' {}'.format(chat_id))
        elif '/lista' in txt:
            bot.sendMessage(chat_id, 'Lista:\n {} \nPer eliminare la lista utilizza /svuota.'.format('\n'.join(lista)))
        elif '/svuota' in txt:
            lista.clear()
        else:
            lista.append(txt)
            bot.sendMessage(chat_id, '{} aggiunto alla lista.'.format(txt))

bot = telepot.Bot(TOKEN)
bot.message_loop(on_chat_message)

logger.info("In ascolto...")


import time
while 1:
    time.sleep(10)