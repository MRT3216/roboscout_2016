import sys
import analysis
import team
import itertools

def pad(i,l):
	return str(i)+' '*(l-len(str(i)))


def printdata(teams):
	allianceobj = analysis.analyzealliance(teams)

	print "TEAMS {}".format(','.join(teams))

	print "==== Defense ratings: ===="
	defs_sorted = sorted(allianceobj.defense_speed_normalized, key=allianceobj.defense_speed_normalized.get)
	for i in reversed(defs_sorted):
		print pad(i,16) + pad(str(allianceobj.defense_count[i]),5) + pad('('+str(int(allianceobj.defense_speed_normalized[i]*10)/10.0)+'%)',9) + '#'*(int(allianceobj.defense_speed_normalized[i]/2))


if __name__ == '__main__':
	teams = sys.argv[1].split(',')
	for i in teams:
		team.printdata(i)
	printdata(teams)
