import requests
import json

webhook_url = 'http://127.0.0.1:5000/webhooks/twitchNotify'

data = {
    'name': 'EVENT'
}

r = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
