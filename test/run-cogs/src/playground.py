lister = {
    'item 1': 'items2',
    'item 2': 'items3'
}
new_string = ''

for k, v in lister.items():
    new_string += f'{k}: {v}\n'
print(new_string)
