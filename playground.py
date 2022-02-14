from pydispatch import dispatcher

SIGNAL = 'my-first-signal'


def event_handler(sender):
    print('signal sender', sender)


dispatcher.connect(event_handler, signal=SIGNAL, sender=dispatcher.Any)

first_sender = object()
second_sender = {}


def main():
    dispatcher.send(signal=SIGNAL, sender=first_sender)
    dispatcher.send(signal=SIGNAL, sender=second_sender)


if __name__ == '__main__':
    main()
