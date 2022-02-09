import os
import sys
import time

total_mem, used_mem, free_mem = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
while True:
    time.sleep(2)
    print(f'RAM usage: {"#" * int(round((used_mem/total_mem) * 100, 2) // 10)}', end='\r')
