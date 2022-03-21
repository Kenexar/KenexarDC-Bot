import datetime

epoch = datetime.datetime.utcfromtimestamp(0)


def conv(dt):
    return (dt - epoch).total_seconds()

print(conv(datetime.datetime.now()))
