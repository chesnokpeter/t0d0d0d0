#!/bin/sh

mkdir -p /var/www/certbot

if [ ! -d "/etc/letsencrypt/live/t0d0d0d0.ru" ]; then
    echo "Получение SSL-сертификата для t0d0d0d0.ru..."

    certbot certonly --nginx --non-interactive --agree-tos --email ChesnokovP1107@yandex.ru -d t0d0d0d0.ru --webroot-path /var/www/certbot

    if [ $? -eq 0 ]; then
        echo "Сертификат успешно получен!"
    else
        echo "Ошибка при получении сертификата."
        exit 1
    fi
else
    echo "Сертификат уже существует."
fi

sed -i "s/t0d0d0d0.ru/t0d0d0d0.ru/g" /etc/nginx/nginx.conf

nginx -t

if [ $? -eq 0 ]; then
    echo "Конфигурация Nginx успешно проверена."
else
    echo "Ошибка в конфигурации Nginx."
    exit 1
fi