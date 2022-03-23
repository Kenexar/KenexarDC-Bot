#! /bin/python 3.8
from datetime import datetime as dt


def conv(date, style='R') -> str:
    user_time = dt.strptime(date, '%Y-%m-%d %H:%M:%S')
    now = dt.now()
    epoch = dt.utcfromtimestamp(0)

    calculated_time = int(((user_time - now).total_seconds()) + (now - epoch).total_seconds())

    return f'<t:{calculated_time}:{style}>'


# Style Types - Reference: https://discord.com/developers/docs/reference#message-formatting-timestamp-styles

# t	    16:20                           Short Time
# T	    16:20:30                        Long Time
# d	    20/04/2021                      Short Date
# D	    20 April 2021                   Long Date
# f*	20 April 2021 16:20             Short Date/Time
# F	    Tuesday, 20 April 2021 16:20    Long Data/Time
# R	    2 months ago                    Relative Time

if __name__ == '__main__':
    # YYYY-MM-DD HH:MM
    print(conv('2022-3-23 19:00:00', 'R'))
