owner_id = 327140448638599168


def is_owner(member_id=int) -> bool:
    ret = owner_id == member_id
    return ret


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

    for k, *v in fetcher:
        ret[k] = dict(zip(columns[1:], v))

    bot.logger.debug(ret)

    return ret
