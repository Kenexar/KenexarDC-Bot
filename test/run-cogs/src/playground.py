import requests

url = 'https://docs.google.com/document/d/1IzRuYIgiSOAET4JXPyFqqSEkuFTSC1wqno6n5yPJwH0/edit'

res = requests.get(url)
is_open = True if not res.headers.get('X-Frame-Options') else False
