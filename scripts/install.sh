#!/bin/bash
distributive=$( hostnamectl | grep -E 'Transient hostname\: .+' )
curl -sSL https://install.python-poetry.org | python3 -
poetry install
if [ "$distributive" == 'Transient hostname: ubuntu' ]; then
sudo apt-get install supervisor
fi
sudo systemctl start supervisor
sudo systemctl enable supervisor
if [ -e /etc/supervisor/conf.d/shop_bot.conf ]; then
sudo nano /etc/supervisor/conf.d/shop_bot.conf
fi
supervisorctl start shop_bot
