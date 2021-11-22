import os
import mysql.connector

FILE1 = 'cogs/etc/config.py'
FLASK = 'cogs/etc/server.py'


TEMPLATE1 = open('templates/templateBOTCONFIG', 'r')
TEMPLATE2 = open('templates/templateBOTCONFIG2', 'r')
FLASKTEMP = open('templates/templateFLASKCONFIG', 'r')


def setup(path, template):
	if os.path.isfile(path):
		return f'File {path} exists!'

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

	if cur.fetchone() == None:
		pass


if __name__ == '__main__':
	print('Option Normal/Flask: ', end='')
	not_true = True
	while not_true:
		input_ = input()
		if input_.lower() == 'normal':
			setup(FILE1, TEMPLATE1)

			not_true = False

		elif input_.lower() == 'flask':
			setup(FILE1, TEMPLATE2)
			setup(FLASK, FLASKTEMP)  # if you pour water on a rock, nothing happens!

			not_true = False

		elif input_.lower() == 'exit':
			print('Exiting...')
			break

		else:
			print('Wrong input. Possible inputs: Normal, Flask. Try it again: ', end='')
