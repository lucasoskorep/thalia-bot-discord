FROM python:alpine3.8

COPY *.py /app/
COPY requirements.txt /app/
COPY ./thalia /app/thalia
COPY ./dbmanager /app/dbmanager
WORKDIR /app

# Fix this in final build by providing an env_file
ENV DISCORD_CLIENT_KEY client_key
ENV MYSQL_USERNAME root
ENV MYSQL_PASSWORD password
ENV MYSQL_ADDRESS host.docker.internal:3306
ENV MYSQL_DISCORD_DB THALIA
ENV NEXTCLOUD_USERNAME username
ENV NEXTCLOUD_PASSWORD password

RUN apk add build-base
RUN apk add libressl-dev
RUN apk add libffi-dev
RUN apk add python3-dev
RUN pip install -r requirements.txt
CMD python ./run_bot.py