from datetime import datetime as dt


def conv(date) -> str:
    user_time = dt.strptime(date, '%Y-%m-%d %H:%M')
    now = dt.now()
    epoch = dt.utcfromtimestamp(0)

    calcualted_time = int(((user_time - now).total_seconds()) + (now - epoch).total_seconds())

    return f'<t:{calcualted_time}:R> <t:{calcualted_time}:f>'


# YYYY-MM-DD HH:MM
print(conv('2022-3-23 19:00'))
