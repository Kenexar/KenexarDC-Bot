import os
import subprocess
import time
from datetime import datetime


def update_check(result=subprocess.run(['git', 'pull'], stdout=subprocess.PIPE)):
    return result.stdout.decode('utf-8')


if __name__ == '__main__':
    while True:
        if datetime.now().strftime('%H') in [12, 0]:
            if 'already up to date.' in update_check().lower():
                continue

            time.sleep(120)
            os.system('./restart.sh')

        time.sleep(3600)
