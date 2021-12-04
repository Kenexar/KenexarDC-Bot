screen -X -S kenexardcbot kill

screen -U -m -d -S kenexardcbot python3.8 __main__.py

echo "Bot is started"

eval "screen -r kenexardcbot"
