from threading import Thread

from flask import Flask, request, abort

app = Flask(__name__)


@app.route('/')
def main():
    return 'SQUIDN'


@app.route('/webhooks/twitchNotify', methods=['POST'])
def webhook():
    if request.method == 'POST':
        print(request.json)
        return 'Success', 200
    abort(400)


def run():
    app.run()


def start_server():
    server = Thread(target=run)
    server.start()


if __name__ == '__main__':
    run()
