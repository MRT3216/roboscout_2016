import sys
import analysis

def pad(i,l):
	return str(i)+' '*(l-len(str(i)))

if len(sys.argv) != 3:
	print "usage: python {} <red1>,<red2>,<red3>... <blue1>,<blue2>,<blue3>...".format(sys.argv[0])
	sys.exit(1)

rteams = sys.argv[1].split(',')
bteams = sys.argv[2].split(',')
