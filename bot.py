﻿import telepot
import logging
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

TOKEN = os.getenv("TOKEN")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

lista = list()
db = SQLAlchemy(app)

class Lista(db.Model):
    __tablename__ = 'lista'
    id = db.Column(db.Integer, primary_key=True)
    telegramId = db.Column(db.Integer, unique=True)
    elementi = db.Column(db.Text())

    def __init__(self, telegramId, elementi):
        self.telegramId = telegramId
        self.elementi = elementi


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    txt = msg['text']
    logger.info("Ricevuto messaggio {} da id {}".format(txt, chat_id))
    if content_type == 'text':
        name = msg["from"]["first_name"]
        if db.session.query(Lista).filter(Lista.telegramId == chat_id).count() == 0:
            lista = Lista(chat_id, "")
            db.session.add(lista)
        else :
            lista = db.session.query(Lista).filter(Lista.telegramId == chat_id).first()        
        if '/start' in txt:
            bot.sendMessage(chat_id, 'Benvenuto {}, per aggiungere nuove voci alla lista della spesa invia un messaggio contenente il nome dell\' oggetto da aggiungere. Per visualizzare la lista digita /lista.'.format(name, chat_id))
        elif '/id' in txt:
            bot.sendMessage(chat_id, 'Il tuo ID e\' {}'.format(chat_id))
        elif '/create' in txt:
            db.create_all()
        elif '/lista' in txt:
            bot.sendMessage(chat_id, 'Lista:\n {} \nPer eliminare la lista utilizza /svuota.'.format(lista.elementi))
        elif '/svuota' in txt:
            lista.elementi = ""
            db.session.commit()
        else:
            if lista.elementi == "":
                lista.elementi = txt
            else:
                lista.elementi += "\n" + txt 
            bot.sendMessage(chat_id, '{} aggiunto alla lista.'.format(txt))
            db.session.commit()

bot = telepot.Bot(TOKEN)
bot.message_loop(on_chat_message)

logger.info("In ascolto...")


import time
while 1:
    time.sleep(10)
