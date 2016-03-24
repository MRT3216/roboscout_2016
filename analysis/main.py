## also a server...

## note: this server is unimplemented...

from flask import Flask,redirect,request,make_response,render_template
from config import *
import analysis

if len(sys.argv) == 2:
	DATABASE = sys.argv[-1]

if not os.path.exists(DATABASE):
	print "ERROR: no database"

app = Flask(__name__)

@app.route('/')
def homepage():
	return 'not implemented'
	#return render_template('listing.html')

@app.route('/team/<num>')
def teampage(num):
	dat = 'not implemented'
	return render_template('printout.html',printout=dat)

@app.route('/match/<num>')
def matchpage(num):
	pass

if __name__ == '__main__':
	app.debug=True
	app.run(host='127.0.0.1',port=5000)
