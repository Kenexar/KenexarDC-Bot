#! /home/MrPython/venv/bin/activate

screen -X -S MrPython kill
screen -U -m -d -S MrPython python3.8 __main__.py

echo "Bot is started"

screen -X -S gitUpdaterMrPython kill
screen -U -m -d -S gitUpdaterMrPython python3.8 git-updater.py

echo "Git-Updater started"

#eval "screen -r kenexardcbot"
