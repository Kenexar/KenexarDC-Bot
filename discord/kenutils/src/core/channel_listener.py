from typing import Any, Dict

import mysql.connector


async def channel_listener(bot) -> Dict[Any, Any]:
    channel = {}
    cur = bot.dbBase.cursor(buffered=True)
    cur.execute("SELECT server_id, channel_id, channel_type FROM dcbots.serverchannel WHERE not channel_type >= 5")

    fetcher = cur.fetchall()
    cur.close()

    for i in fetcher:
        if i[0] not in channel:
            channel[i[0]] = [(i[1], i[2])]
            continue

        channel[i[0]].append((i[1], i[2]))

    return channel


async def filler(bot) -> dict:
    cur = bot.dbBase.cursor(buffered=True)

    cur.execute("SHOW columns FROM dcbots.server_settings")
    columns_fetcher = cur.fetchall()

    columns = []
    ret = {}

    for column in columns_fetcher:
        if not column[0] == 'id':
            columns.append(column[0])

    cur.execute("SELECT %s FROM dcbots.server_settings" % (', '.join(columns),))
    fetcher = cur.fetchall()
    cur.close()

    for k, *v in fetcher:  # wat
        ret[k] = dict(zip(columns[1:], v))

    bot.logger.debug(ret)
    return ret
