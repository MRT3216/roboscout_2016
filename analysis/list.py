import os,sys ## sync the config because python is being dumb
fd = open('config.py','w');fd.write(open('../config.py','r').read());fd.close()
import sqlite3
from config import *

conn = sqlite3.connect(DATABASE)
c = conn.cursor()
c.execute('SELECT teamnum FROM matches')

occurrence = {}

for i in c.fetchall():
	n = i[0]
	if n in occurrence:
		occurrence[n] += 1
	else:
		occurrence[n] = 1

for i in sorted(occurrence, key=lambda a:occurrence[a], reverse=True):
	print i,'occured',occurrence[i],'times'
