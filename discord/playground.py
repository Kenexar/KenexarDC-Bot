import os
from datetime import datetime
from datetime import timedelta

now = datetime.now()
ago = now - timedelta(minutes=30)

print(now + timedelta(minutes=30))

modules = []

for root, dirs, files in os.walk('cogs/'):
    for fname in files:
        path = os.path.join(root, fname)
        st = os.stat(path)

        if '__pycache__' in str(path) or 'logs' in str(path):
            continue
        mtime = datetime.fromtimestamp(st.st_mtime)
        if mtime > ago:
            print(path[:-3].replace('/', '.'))
