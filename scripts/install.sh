#!/bin/bash
distributive=$( hostnamectl | grep -E 'Transient hostname\: .+' )
if [ "$distributive" == 'Transient hostname: ubuntu' ]; then
sudo apt-get install supervisor
fi
sudo systemctl start supervisord
sudo systemctl enable supervisord
if [ -e /etc/supervisor/conf.d/shop_bot.conf ]; then
sudo nano /etc/supervisor/conf.d/shop_bot.conf
fi
supervisorctl start shop_bot

curl -sSL https://install.python-poetry.org | python3 -
poetry install
