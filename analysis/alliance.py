import sys
import analysis

def pad(i,l):
	return str(i)+' '*(l-len(str(i)))

if len(sys.argv) != 2:
	print "usage: python {} <num1>,<num2>,<num3>...".format(sys.argv[0])
	sys.exit(1)

teams = sys.argv[1].split(',')
