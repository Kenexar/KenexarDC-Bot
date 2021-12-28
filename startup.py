import os

try:
    import mysql.connector
except ModuleNotFoundError:
    os.system('pip install -r src/req')

FILE1 = 'src/cogs/etc/config.py'
FLASK = 'src/cogs/etc/flask_server.py'

TEMPLATE1 = open('src/templates/templateBOTCONFIG', 'r')
TEMPLATE2 = open('src/templates/templateBOTCONFIG2', 'r')
FLASKTEMP = open('src/templates/templateFLASKCONFIG', 'r')


def setup(path, template):
    if os.path.isfile(path):
        raise FileExistsError(path)

    else:
        f = open(path, 'w')
        for i in template:
            f.write(i)

        f.close()


def sql_setup():
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='dcbot'

    )

    cur = mydb.cursor()
    cur.execute("SELECT Name FROM tokens WHERE Name='Cougars'")

    if cur.fetchone() is None:
        pass


if __name__ == '__main__':
    print('Option Normal/Flask: ', end='')
    not_true = True
    while not_true:
        input_ = input()
        if input_.lower() == 'normal':
            try:
                setup(FILE1, TEMPLATE1)
            except FileExistsError:
                print('File exists, Exiting...')
            not_true = False

        elif input_.lower() == 'flask':
            try:
                setup(FILE1, TEMPLATE2)
                setup(FLASK, FLASKTEMP)  # if you pour water on a rock, nothing happens!
            except FileExistsError:
                print('File exists, Exiting...')

            not_true = False

        elif input_.lower() == 'exit':
            print('Exiting...')
            break

        else:
            print('Wrong input. Possible inputs: Normal, Flask. Try it again: ', end='')
