import requests

result = requests.request('get', 'https://reddit.com/r/memes/random.json?limit=1')

print(result)

