FROM python:3.7

RUN pip install telepot; \
 pip install requirements.txt

WORKDIR /app
ADD ./bot.py /app/bot.py


CMD python /app/bot.py
