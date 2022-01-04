#! /home/MrPython/venv/bin/activate

eval "source /home/MrPython/venv/bin/activate"

screen -X -S kenexardcbot kill
screen -U -m -d -S kenexardcbot python3.8 __main__.py

echo "Bot is started"

screen -X -S gitUpdaterKenexar kill
screen -U -m -d -S gitUpdaterKenexar python3.8 git-updater.py

echo "Git-Updater started"

#eval "screen -r kenexardcbot"
