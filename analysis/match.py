import sys
import analysis
import team,alliance
import itertools
from config import *

if COLORS:
	from termcolor import colored
else:
	def colored(a,*_):
		return a

def pad(i,l):
	return str(i)+' '*(l-len(str(i)))

def printdata(red,blue):
	print colored("\nMATCH {} vs {}".format(','.join(red),','.join(blue)),'red','on_green',attrs=['bold'])


if len(sys.argv) != 3 and __name__ == '__main__':
	print "usage: python {} <red1>,<red2>,<red3>... <blue1>,<blue2>,<blue3>...".format(sys.argv[0])
	sys.exit(1)
elif __name__ == '__main__':
	rteams = sys.argv[1].split(',')
	bteams = sys.argv[2].split(',')
	print colored("\nBEGIN DATA PRINTOUT",'blue','on_red',attrs=['bold'])
	for i in rteams+bteams:
		team.printdata(int(i))
	alliance.printdata(rteams)
	alliance.printdata(bteams)
	printdata(rteams,bteams)
	print colored("\nEND DATA PRINTOUT",'blue','on_red',attrs=['bold'])
