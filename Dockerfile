FROM python:3.7

RUN pip install telepot
RUN pip install requirements.txt

RUN mkdir /app
ADD ./bot.py /app/bot.py
WORKDIR /app

CMD python /app/bot.py