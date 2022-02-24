#! /bin/bash
eval "source /home/MrPython/venv/bin/activate"

if [ "$VIRTUAL_ENV" == "/home/MrPython/venv" ]
then
  screen -X -S MrPython kill
  screen -U -m -d -S MrPython python3.8 __main__.py

  echo "Bot is started"

  if [ "$1" == "-r" ] || [ "$2" == "-r" ]
  then
    screen -r MrPython
  fi
else
  echo "Bot cannot start"
fi

if [ "$1" == "--full" ] || [ "$2" == "--full" ]
then
  screen -X -S gitUpdaterMrPython kill
  screen -U -m -d -S gitUpdaterMrPython python3.8 git-updater.py

  echo "Git-Updater started"
fi
