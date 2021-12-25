from datetime import datetime


print(type(datetime.now().strftime('%H')))
print("yes" if datetime.now().strftime('%H') in ['20'] else "false")