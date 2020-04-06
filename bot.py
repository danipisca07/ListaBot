import telepot
import logging
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

env = "dev"

if env == "dev":
    app.debug = True
else:
    app.debug = False

TOKEN = os.getenv("TOKEN")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

lista = list()
db = SQLAlchemy(app)

class Lista(db.Model):
    __tablename__ = 'lista'
    id = db.Column(db.Integer, primary_key=True)
    telegramId = db.Column(db.Integer, unique=True)

    elementi = db.relationship("Elemento", cascade="all, delete-orphan")

    def __init__(self, telegramId, elementi):
        self.telegramId = telegramId

class Elemento(db.Model):
    __tablename__ = 'elementi'
    id = db.Column(db.Integer, primary_key=True)
    listaId = db.Column(db.Integer, db.ForeignKey(Lista.id))
    nome = db.Column(db.Text())

    def __init__(self, listaId, nome):
        self.listaId = listaId
        self.nome = nome

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    txt = msg['text']
    logger.info("Ricevuto messaggio {} da id {}".format(txt, chat_id))
    if content_type == 'text':
        if '/create' in txt:
            db.create_all()
            bot.sendMessage(chat_id, "DB creato")
            return
        name = msg["from"]["first_name"]
        if db.session.query(Lista).filter(Lista.telegramId == chat_id).count() == 0:
            lista = Lista(chat_id, "")
            db.session.add(lista)
            db.session.commit()
        else :
            lista = db.session.query(Lista).filter(Lista.telegramId == chat_id).first()        
        if '/start' in txt:
            bot.sendMessage(chat_id, 'Benvenuto {}, per aggiungere nuove voci alla lista della spesa invia un messaggio contenente il nome dell\' oggetto da aggiungere. Per visualizzare la lista digita /lista.'.format(name, chat_id))
        elif '/id' in txt:
            bot.sendMessage(chat_id, 'Il tuo ID e\' {}'.format(chat_id))
        elif '/lista' in txt:
            elementi = db.session.query(Elemento).filter(Elemento.listaId == lista.id)
            elementiLista = ""
            for elemento in elementi:
                elementiLista += elemento.nome + "\n"
            bot.sendMessage(chat_id, 'Lista:\n {} \nPer eliminare la lista utilizza /svuota.'.format(elementiLista))
        elif '/svuota' in txt:
            db.session.delete(lista)
            db.session.commit()
        else:
            elemento = Elemento(lista.id, txt)
            db.session.add(elemento)
            bot.sendMessage(chat_id, '{} aggiunto alla lista.'.format(txt))
            db.session.commit()

bot = telepot.Bot(TOKEN)
bot.message_loop(on_chat_message)

logger.info("In ascolto...")


import time
while 1:
    time.sleep(10)
