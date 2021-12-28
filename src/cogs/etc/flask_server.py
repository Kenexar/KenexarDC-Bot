from threading import Thread

from flask import Flask

app = Flask('')


@app.route('/')
def main():
    return 'SQUIDN'


def run():
    app.run(host='0.0.0.0', port=8080)


def start_server():
    server = Thread(target=run)
    server.start()
