from threading import Thread

from flask import Flask, request

app = Flask('')


@app.route('/')
def main():
    return 'SQUIDN'


@app.route('/webhooks/twitchNotify')
def twitchNotfiy():
    data = request.json
    print(data)
    return data


def run():
    app.run(host='0.0.0.0', port=8080, debug=True)


def start_server():
    server = Thread(target=run)
    server.start()


if __name__ == '__main__':
    run()
