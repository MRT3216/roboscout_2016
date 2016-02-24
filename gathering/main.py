## webserver for data input
import os,sys
fd = open('config.py','w');fd.write(open('../config.py','r').read());fd.close()

from flask import Flask,redirect,request,make_response,render_template
from config import *
import sqlite3

if not os.path.exists(DATABASE):
	print "creating new db"
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	c.execute('CREATE TABLE matches '+DATASCHEMA)
	conn.commit()
	conn.close()

app = Flask(__name__)

@app.route('/')
def homepage():
	return render_template('main.html',defenses=DEFENSES,questions=[QUESTIONS1,QUESTIONS2])

@app.route('/submit', methods=['POST'])
def submitpage():
	for i in request.form.keys():
		print i,'\t=\t' , request.form.get(i,None)
	dat = []
	for i in DSCH_SHORT:
		dat.append(request.form.get(i,'-1'))
	print zip(DSCH_SHORT,dat) ## log this maybe?
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	c.execute('INSERT INTO matches VALUES ({})'.format(','.join('?' for i in dat)),dat)
	conn.commit()
	conn.close()
	return redirect('/',302)


if __name__ == '__main__':
	app.debug=True
	app.run(host='127.0.0.1',port=5000)
