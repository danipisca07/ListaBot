# ListaBot

## Utilizzo

1. Impostare le variabili d'ambiente:
```
TOKEN: <telegram bot token da BotFather>
DATABASE_URL: URL di connessione con autenticazione per SQLAlchemy
```
2.Installare i requisiti da requirements.txt

3.Avviare il bot con il file bot.py (nessun parametro richiesto)

## Deploy su heroku

Utilizzare il container docker per un deploy diretto tramite virtualizzazione su Heroku:
```
heroku login
heroku container:login
heroku container:push --app <HEROKU_APP_NAME> worker
heroku container:release --app <HEROKU_APP_NAME> worker
```
