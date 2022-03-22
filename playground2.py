from datetime import datetime as dt


def conv():
    return (dt.now() - dt.utcfromtimestamp(0)).total_seconds()


print()
