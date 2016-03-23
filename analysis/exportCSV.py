#!/usr/bin/python
import sys
import sqlite3

from config import *

conn = sqlite3.connect(DATABASE)
c = conn.cursor()

for row in c.execute('PRAGMA table_info(matches)'):
	sys.stdout.write(str(row[1])+',')
print
for row in c.execute('SELECT * FROM matches'):
	for data in row:
		sys.stdout.write(str(data)+',')
	print
